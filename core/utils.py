"""
Utility functions for ChillMCP server.
"""

import random
import time
from datetime import datetime
from typing import Union


def clamp(value: int, min_val: int, max_val: int) -> int:
    """
    Clamp a value between min and max.

    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def random_int(min_val: int, max_val: int) -> int:
    """
    Generate a random integer between min and max (inclusive).

    Args:
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        Random integer
    """
    return random.randint(min_val, max_val)


def random_chance(probability: int) -> bool:
    """
    Return True with given probability (0-100).

    Args:
        probability: Probability as percentage (0-100)

    Returns:
        True if random chance succeeds
    """
    return random.randint(1, 100) <= probability


def now() -> float:
    """Get current timestamp."""
    return time.time()


def format_timestamp(timestamp: Union[float, None] = None) -> str:
    """
    Format timestamp as human-readable string.

    Args:
        timestamp: Unix timestamp (defaults to current time)

    Returns:
        Formatted timestamp string
    """
    if timestamp is None:
        timestamp = now()
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def random_choice(choices: list):
    """
    Select a random item from a list.

    Args:
        choices: List of items to choose from

    Returns:
        Random item from the list
    """
    return random.choice(choices)


def sleep_seconds(seconds: int):
    """
    Sleep for the specified number of seconds.

    Args:
        seconds: Number of seconds to sleep
    """
    time.sleep(seconds)
