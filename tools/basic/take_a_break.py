"""
Basic break tool: take_a_break
Just a simple break to relax.
"""

from tools.base import BaseTool
from core.utils import random_choice


class TakeABreakTool(BaseTool):
    """Basic break tool for general relaxation."""

    def get_name(self) -> str:
        return "take_a_break"

    def get_description(self) -> str:
        return "Take a basic break to reduce stress and relax"

    def get_emoji(self) -> str:
        return "🌴"

    def get_message(self) -> str:
        messages = [
            "Taking a quick break to relax...",
            "Stepping away for a moment of peace...",
            "Chilling out for a bit...",
            "Taking some time to decompress...",
            "Having a moment of zen..."
        ]
        return random_choice(messages)

    def get_break_summary(self) -> str:
        return "Basic relaxation break"
