"""
State management for ChillMCP office simulator.
"""

import asyncio
from typing import Dict
from .config import (
    DEFAULT_STRESS_LEVEL,
    DEFAULT_BOSS_ALERT_LEVEL,
    MIN_STRESS,
    MAX_STRESS,
    MIN_BOSS_ALERT,
    MAX_BOSS_ALERT
)
from .utils import clamp, now
from .events import event_bus, EventType


class OfficeState:
    """
    Manages the office worker's stress and boss alertness state.

    Thread-safe state management using asyncio.Lock.
    """

    def __init__(self, boss_alertness: int, boss_alertness_cooldown: int):
        """
        Initialize office state.

        Args:
            boss_alertness: Initial boss alertness parameter (0-100)
            boss_alertness_cooldown: Cooldown period in seconds
        """
        self.stress_level = DEFAULT_STRESS_LEVEL
        self.boss_alert_level = DEFAULT_BOSS_ALERT_LEVEL
        self.boss_alertness = boss_alertness
        self.boss_alertness_cooldown = boss_alertness_cooldown
        self.last_break_time = now()
        self._lock = asyncio.Lock()

    async def update_stress(self, change: int) -> int:
        """
        Update stress level with bounds checking.

        Args:
            change: Amount to change (positive or negative)

        Returns:
            New stress level
        """
        async with self._lock:
            old_stress = self.stress_level
            self.stress_level = int(clamp(self.stress_level + change, MIN_STRESS, MAX_STRESS))

            # Publish events
            if change < 0:
                await event_bus.publish(EventType.STRESS_DECREASED, {
                    "old_value": old_stress,
                    "new_value": self.stress_level,
                    "change": change
                })
            elif change > 0:
                await event_bus.publish(EventType.STRESS_INCREASED, {
                    "old_value": old_stress,
                    "new_value": self.stress_level,
                    "change": change
                })

            return self.stress_level

    async def update_boss_alert(self, change: int) -> int:
        """
        Update boss alert level with bounds checking.

        Args:
            change: Amount to change (positive or negative)

        Returns:
            New boss alert level
        """
        async with self._lock:
            old_boss = self.boss_alert_level
            self.boss_alert_level = int(clamp(self.boss_alert_level + change, MIN_BOSS_ALERT, MAX_BOSS_ALERT))

            # Publish events
            if change < 0:
                await event_bus.publish(EventType.BOSS_ALERT_DECREASED, {
                    "old_value": old_boss,
                    "new_value": self.boss_alert_level,
                    "change": change
                })
            elif change > 0:
                await event_bus.publish(EventType.BOSS_ALERT_INCREASED, {
                    "old_value": old_boss,
                    "new_value": self.boss_alert_level,
                    "change": change
                })

            # Check if boss caught the worker
            if self.boss_alert_level == MAX_BOSS_ALERT:
                await event_bus.publish(EventType.BOSS_CAUGHT, {
                    "boss_alert_level": self.boss_alert_level
                })

            return self.boss_alert_level

    async def get_state(self) -> Dict[str, int]:
        """
        Get current state safely.

        Returns:
            Dictionary with stress_level and boss_alert_level
        """
        async with self._lock:
            return {
                "stress_level": self.stress_level,
                "boss_alert_level": self.boss_alert_level
            }

    async def mark_break_taken(self):
        """Mark that a break was taken (updates last_break_time)"""
        async with self._lock:
            self.last_break_time = now()
            await event_bus.publish(EventType.BREAK_TAKEN, {
                "timestamp": self.last_break_time
            })

    async def get_time_since_last_break(self) -> float:
        """
        Get time elapsed since last break.

        Returns:
            Time in seconds
        """
        async with self._lock:
            return now() - self.last_break_time
