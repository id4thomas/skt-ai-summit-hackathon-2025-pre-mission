"""
Utility functions for ChillMCP.
"""

import random
import time
from typing import Union


def clamp(value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> Union[int, float]:
    """
    Clamp a value between min and max bounds.

    Args:
        value: The value to clamp
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def rand(min_val: int, max_val: int) -> int:
    """
    Generate a random integer between min and max (inclusive).

    Args:
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        Random integer
    """
    return random.randint(min_val, max_val)


def now() -> float:
    """
    Get current timestamp.

    Returns:
        Current time in seconds since epoch
    """
    return time.time()
