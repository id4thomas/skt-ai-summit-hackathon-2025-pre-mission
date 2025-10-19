"""
Core module for ChillMCP.
"""

from .config import *
from .state import OfficeState
from .scheduler import (
    stress_increase_loop,
    boss_alert_decrease_loop,
    check_boss_and_delay,
    start_background_tasks
)
from .events import event_bus, EventType, EventBus
from .validators import format_response, validate_response
from .utils import clamp, rand, now

__all__ = [
    # Config
    'DEFAULT_STRESS_LEVEL',
    'DEFAULT_BOSS_ALERT_LEVEL',
    'MIN_STRESS',
    'MAX_STRESS',
    'MIN_BOSS_ALERT',
    'MAX_BOSS_ALERT',
    'STRESS_INCREASE_INTERVAL',
    'STRESS_INCREASE_AMOUNT',
    'BOSS_CAUGHT_DELAY',
    'MIN_BOSS_ALERTNESS',
    'MAX_BOSS_ALERTNESS',
    'MIN_COOLDOWN',
    # State
    'OfficeState',
    # Scheduler
    'stress_increase_loop',
    'boss_alert_decrease_loop',
    'check_boss_and_delay',
    'start_background_tasks',
    # Events
    'event_bus',
    'EventType',
    'EventBus',
    # Validators
    'format_response',
    'validate_response',
    # Utils
    'clamp',
    'rand',
    'now',
]
