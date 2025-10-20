"""
Scheduler module for ChillMCP server.
Handles automatic stress increase and boss alert cooldown.
"""

import threading
import time
from typing import Callable, Optional

from core.state import AgentState


class StateScheduler:
    """
    Background scheduler that automatically updates agent state.
    Runs stress auto-increment and boss alert cooldown in separate thread.
    """

    def __init__(self, state: AgentState, update_interval: int = 1):
        """
        Initialize scheduler.

        Args:
            state: AgentState instance to manage
            update_interval: How often to check for updates (seconds)
        """
        self.state = state
        self.update_interval = update_interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._callbacks = {
            'stress_update': [],
            'boss_alert_update': []
        }

    def register_callback(self, event: str, callback: Callable):
        """
        Register a callback for state update events.

        Args:
            event: Event type ('stress_update' or 'boss_alert_update')
            callback: Function to call when event occurs
        """
        if event in self._callbacks:
            self._callbacks[event].append(callback)

    def _notify(self, event: str, *args, **kwargs):
        """Notify all callbacks for an event."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                # Log error but don't crash scheduler
                print(f"Error in callback for {event}: {e}")

    def _run(self):
        """Main scheduler loop."""
        while self._running:
            try:
                # Check for stress auto-increase
                new_stress = self.state.auto_update_stress()
                if new_stress is not None:
                    self._notify('stress_update', new_stress)

                # Check for boss alert cooldown
                new_boss_alert = self.state.auto_decrease_boss_alert()
                if new_boss_alert is not None:
                    self._notify('boss_alert_update', new_boss_alert)

            except Exception as e:
                print(f"Error in scheduler loop: {e}")

            # Sleep for update interval
            time.sleep(self.update_interval)

    def start(self):
        """Start the scheduler in background thread."""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the scheduler."""
        if not self._running:
            return

        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
            self._thread = None

    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self._running

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False
