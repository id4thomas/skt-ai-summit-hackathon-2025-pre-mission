"""
Event system for ChillMCP server.
Simple pub/sub implementation for state change notifications.
"""

from typing import Callable, Dict, List


class EventBus:
    """Simple event bus for publishing and subscribing to events."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event: str, callback: Callable):
        """
        Subscribe to an event.

        Args:
            event: Event name
            callback: Function to call when event is published
        """
        if event not in self._subscribers:
            self._subscribers[event] = []
        self._subscribers[event].append(callback)

    def unsubscribe(self, event: str, callback: Callable):
        """
        Unsubscribe from an event.

        Args:
            event: Event name
            callback: Callback function to remove
        """
        if event in self._subscribers:
            try:
                self._subscribers[event].remove(callback)
            except ValueError:
                pass

    def publish(self, event: str, *args, **kwargs):
        """
        Publish an event to all subscribers.

        Args:
            event: Event name
            *args: Positional arguments to pass to callbacks
            **kwargs: Keyword arguments to pass to callbacks
        """
        if event in self._subscribers:
            for callback in self._subscribers[event]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"Error in event callback for {event}: {e}")

    def clear(self, event: str = None):
        """
        Clear all subscribers for an event, or all events if event is None.

        Args:
            event: Event name to clear (None clears all)
        """
        if event is None:
            self._subscribers.clear()
        elif event in self._subscribers:
            self._subscribers[event].clear()


# Global event bus instance
event_bus = EventBus()


# Event names
STRESS_UPDATED = "stress_updated"
BOSS_ALERT_UPDATED = "boss_alert_updated"
TOOL_EXECUTED = "tool_executed"
DELAY_TRIGGERED = "delay_triggered"
