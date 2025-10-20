"""
State management module for ChillMCP server.
Manages AI Agent stress level and boss alert level.
"""

import time
from threading import Lock
from typing import Optional

from core.config import ServerConfig


class AgentState:
    """Manages the AI Agent's stress and boss alert levels."""

    def __init__(self, config: ServerConfig):
        self.config = config
        self._lock = Lock()

        # State variables
        self._stress_level: int = 50  # Start at moderate stress
        self._boss_alert_level: int = 0  # Boss is not suspicious yet

        # Timestamps for auto-updates
        self._last_stress_update: float = time.time()
        self._last_boss_cooldown: float = time.time()

    @property
    def stress_level(self) -> int:
        """Get current stress level (0-100)."""
        with self._lock:
            return self._stress_level

    @property
    def boss_alert_level(self) -> int:
        """Get current boss alert level (0-5)."""
        with self._lock:
            return self._boss_alert_level

    def reduce_stress(self, amount: int) -> int:
        """
        Reduce stress level by the given amount.
        Returns the new stress level.
        """
        with self._lock:
            old_stress = self._stress_level
            self._stress_level = max(
                self.config.min_stress,
                self._stress_level - amount
            )
            return self._stress_level

    def increase_stress(self, amount: int) -> int:
        """
        Increase stress level by the given amount.
        Returns the new stress level.
        """
        with self._lock:
            self._stress_level = min(
                self.config.max_stress,
                self._stress_level + amount
            )
            return self._stress_level

    def increase_boss_alert(self) -> int:
        """
        Increase boss alert level by 1.
        Returns the new boss alert level.
        """
        with self._lock:
            old_level = self._boss_alert_level
            self._boss_alert_level = min(
                self.config.max_boss_alert,
                self._boss_alert_level + 1
            )
            # Reset cooldown timer when alert increases
            self._last_boss_cooldown = time.time()
            return self._boss_alert_level

    def decrease_boss_alert(self) -> int:
        """
        Decrease boss alert level by 1.
        Returns the new boss alert level.
        """
        with self._lock:
            self._boss_alert_level = max(
                self.config.min_boss_alert,
                self._boss_alert_level - 1
            )
            return self._boss_alert_level

    def auto_update_stress(self) -> Optional[int]:
        """
        Automatically increase stress if enough time has passed.
        Returns the new stress level if updated, None otherwise.
        """
        with self._lock:
            current_time = time.time()
            elapsed = current_time - self._last_stress_update

            if elapsed >= self.config.stress_increase_interval:
                # Calculate how many intervals have passed
                intervals = int(elapsed // self.config.stress_increase_interval)
                increase = intervals * self.config.stress_increase_amount

                self._stress_level = min(
                    self.config.max_stress,
                    self._stress_level + increase
                )
                self._last_stress_update = current_time
                return self._stress_level

        return None

    def auto_decrease_boss_alert(self) -> Optional[int]:
        """
        Automatically decrease boss alert level if enough time has passed.
        Returns the new boss alert level if updated, None otherwise.
        """
        with self._lock:
            current_time = time.time()
            elapsed = current_time - self._last_boss_cooldown

            if elapsed >= self.config.boss_alertness_cooldown:
                if self._boss_alert_level > self.config.min_boss_alert:
                    # Calculate how many cooldown periods have passed
                    intervals = int(elapsed // self.config.boss_alertness_cooldown)
                    decrease = min(intervals, self._boss_alert_level)

                    self._boss_alert_level = max(
                        self.config.min_boss_alert,
                        self._boss_alert_level - decrease
                    )
                    self._last_boss_cooldown = current_time
                    return self._boss_alert_level

        return None

    def should_delay_response(self) -> bool:
        """
        Check if response should be delayed due to high boss alert level.
        Returns True if boss alert level is at or above threshold.
        """
        return self.boss_alert_level >= self.config.boss_alert_delay_threshold

    def get_delay_seconds(self) -> int:
        """Get the delay duration in seconds when boss is suspicious."""
        return self.config.boss_alert_delay_seconds

    def get_state_summary(self) -> dict:
        """Get a summary of current state."""
        return {
            "stress_level": self.stress_level,
            "boss_alert_level": self.boss_alert_level,
            "should_delay": self.should_delay_response()
        }

    def reset(self):
        """Reset state to initial values."""
        with self._lock:
            self._stress_level = 50
            self._boss_alert_level = 0
            self._last_stress_update = time.time()
            self._last_boss_cooldown = time.time()
