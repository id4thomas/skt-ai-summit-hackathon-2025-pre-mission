"""
Validators and response formatters for ChillMCP server.
"""

import re
from typing import Optional, Tuple


def build_tool_response(
    emoji: str,
    message: str,
    break_summary: str,
    stress_level: int,
    boss_alert_level: int
) -> dict:
    """
    Build standardized MCP tool response.

    Args:
        emoji: Emoji to display
        message: Main message text
        break_summary: Summary of the break activity
        stress_level: Current stress level (0-100)
        boss_alert_level: Current boss alert level (0-5)

    Returns:
        MCP-compatible response dictionary
    """
    response_text = f"""{emoji} {message}

Break Summary: {break_summary}
Stress Level: {stress_level}
Boss Alert Level: {boss_alert_level}"""

    return {
        "content": [
            {
                "type": "text",
                "text": response_text
            }
        ]
    }


def parse_response(response_text: str) -> Optional[dict]:
    """
    Parse tool response text and extract structured data.

    Args:
        response_text: Response text to parse

    Returns:
        Dictionary with parsed values or None if parsing fails
    """
    # Extract Break Summary
    break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
    break_match = re.search(break_summary_pattern, response_text, re.MULTILINE)

    # Extract Stress Level
    stress_pattern = r"Stress Level:\s*(\d{1,3})"
    stress_match = re.search(stress_pattern, response_text)

    # Extract Boss Alert Level
    boss_pattern = r"Boss Alert Level:\s*([0-5])"
    boss_match = re.search(boss_pattern, response_text)

    if not (break_match and stress_match and boss_match):
        return None

    try:
        stress_level = int(stress_match.group(1))
        boss_alert_level = int(boss_match.group(1))

        if not (0 <= stress_level <= 100):
            return None

        if not (0 <= boss_alert_level <= 5):
            return None

        return {
            "break_summary": break_match.group(1).strip(),
            "stress_level": stress_level,
            "boss_alert_level": boss_alert_level
        }
    except (ValueError, IndexError):
        return None


def validate_response(response_text: str) -> Tuple[bool, str]:
    """
    Validate tool response format.

    Args:
        response_text: Response text to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    parsed = parse_response(response_text)

    if parsed is None:
        return False, "Failed to parse response or missing required fields"

    stress_level = parsed["stress_level"]
    boss_alert_level = parsed["boss_alert_level"]

    if not (0 <= stress_level <= 100):
        return False, f"Stress Level out of range: {stress_level}"

    if not (0 <= boss_alert_level <= 5):
        return False, f"Boss Alert Level out of range: {boss_alert_level}"

    return True, "Valid response"


def format_delay_warning(seconds: int) -> str:
    """
    Format a warning message about response delay.

    Args:
        seconds: Number of seconds of delay

    Returns:
        Formatted warning message
    """
    return f"⚠️ Boss is watching! Waiting {seconds} seconds to avoid suspicion..."
