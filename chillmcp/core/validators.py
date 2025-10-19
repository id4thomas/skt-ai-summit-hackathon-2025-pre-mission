"""
Response format validators and builders for ChillMCP.
"""

import re
from typing import Dict, Optional


# Validation patterns (from requirements)
BREAK_SUMMARY_PATTERN = r"Break Summary:\s*(.+?)(?:\n|$)"
STRESS_LEVEL_PATTERN = r"Stress Level:\s*(\d{1,3})"
BOSS_ALERT_PATTERN = r"Boss Alert Level:\s*([0-5])"


def format_response(activity: str, stress: int, boss: int) -> str:
    """
    Format standard response with required fields.

    Args:
        activity: Description of the activity/break
        stress: Current stress level (0-100)
        boss: Current boss alert level (0-5)

    Returns:
        Formatted response string
    """
    return f"💬 Break Summary: {activity}\nStress Level: {stress}\nBoss Alert Level: {boss}"


def validate_response(response_text: str) -> Dict[str, any]:
    """
    Validate response format and extract values.

    Args:
        response_text: The response string to validate

    Returns:
        Dictionary with:
            - valid: bool
            - stress_level: int or None
            - boss_alert_level: int or None
            - break_summary: str or None
            - errors: list of error messages
    """
    result = {
        "valid": True,
        "stress_level": None,
        "boss_alert_level": None,
        "break_summary": None,
        "errors": []
    }

    # Check for Break Summary
    summary_match = re.search(BREAK_SUMMARY_PATTERN, response_text)
    if not summary_match:
        result["valid"] = False
        result["errors"].append("Missing Break Summary")
    else:
        result["break_summary"] = summary_match.group(1)

    # Check for Stress Level
    stress_match = re.search(STRESS_LEVEL_PATTERN, response_text)
    if not stress_match:
        result["valid"] = False
        result["errors"].append("Missing Stress Level")
    else:
        stress_value = int(stress_match.group(1))
        if 0 <= stress_value <= 100:
            result["stress_level"] = stress_value
        else:
            result["valid"] = False
            result["errors"].append(f"Stress Level out of range (0-100): {stress_value}")

    # Check for Boss Alert Level
    boss_match = re.search(BOSS_ALERT_PATTERN, response_text)
    if not boss_match:
        result["valid"] = False
        result["errors"].append("Missing Boss Alert Level")
    else:
        boss_value = int(boss_match.group(1))
        if 0 <= boss_value <= 5:
            result["boss_alert_level"] = boss_value
        else:
            result["valid"] = False
            result["errors"].append(f"Boss Alert Level out of range (0-5): {boss_value}")

    return result
