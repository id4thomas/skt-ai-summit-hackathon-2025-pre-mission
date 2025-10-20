"""
Advanced tool: bathroom_break
Pretend to go to the bathroom and browse phone.
"""

from tools.base import BaseTool
from core.utils import random_choice


class BathroomBreakTool(BaseTool):
    """Bathroom break with phone browsing."""

    def get_name(self) -> str:
        return "bathroom_break"

    def get_description(self) -> str:
        return "Pretend to go to bathroom and browse phone for stress relief"

    def get_emoji(self) -> str:
        return "🚽"

    def get_message(self) -> str:
        messages = [
            "Bathroom time! Scrolling through phone... 📱",
            "Nature calls! Time to check social media... 🚽📱",
            "Quick bathroom break with some phone time...",
            "Bathroom escape! Catching up on notifications...",
            "Restroom break - phone browsing in progress..."
        ]
        return random_choice(messages)

    def get_break_summary(self) -> str:
        summaries = [
            "Bathroom break with phone browsing",
            "Restroom escape - mobile device usage",
            "Bathroom time - social media check",
            "Toilet break with smartphone"
        ]
        return random_choice(summaries)
