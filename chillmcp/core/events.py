"""
Event system for ChillMCP (Pub/Sub pattern).
"""

import asyncio
from typing import Callable, List, Dict, Any
from enum import Enum


class EventType(Enum):
    """Event types in the system"""
    STRESS_INCREASED = "stress_increased"
    STRESS_DECREASED = "stress_decreased"
    BOSS_ALERT_INCREASED = "boss_alert_increased"
    BOSS_ALERT_DECREASED = "boss_alert_decreased"
    BOSS_CAUGHT = "boss_caught"  # When boss_alert_level reaches 5
    BREAK_TAKEN = "break_taken"


class EventBus:
    """Simple event bus for pub/sub pattern"""

    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {}

    def subscribe(self, event_type: EventType, callback: Callable):
        """
        Subscribe to an event type.

        Args:
            event_type: The type of event to subscribe to
            callback: Async function to call when event occurs
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: EventType, callback: Callable):
        """
        Unsubscribe from an event type.

        Args:
            event_type: The type of event
            callback: The callback to remove
        """
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)

    async def publish(self, event_type: EventType, data: Dict[str, Any] = None):
        """
        Publish an event to all subscribers.

        Args:
            event_type: The type of event
            data: Optional event data
        """
        if event_type not in self._subscribers:
            return

        data = data or {}
        for callback in self._subscribers[event_type]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                # Log error but don't stop other subscribers
                print(f"Error in event handler: {e}")


# Global event bus instance
event_bus = EventBus()
