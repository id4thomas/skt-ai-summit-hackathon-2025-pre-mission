"""
Advanced tool: urgent_call
Pretend to receive an urgent call and step outside.
"""

from tools.base import BaseTool
from core.utils import random_choice


class UrgentCallTool(BaseTool):
    """Fake urgent call to step outside."""

    def get_name(self) -> str:
        return "urgent_call"

    def get_description(self) -> str:
        return "Pretend to receive urgent call and step outside for fresh air"

    def get_emoji(self) -> str:
        return "📞"

    def get_message(self) -> str:
        messages = [
            "Important call coming in! Stepping outside... 📞",
            "Urgent call! Need to take this outside for privacy...",
            "Phone ringing! Better answer this away from my desk...",
            "Critical call! Taking this outside... (and getting fresh air)",
            "Emergency call! Must handle this outside immediately..."
        ]
        return random_choice(messages)

    def get_break_summary(self) -> str:
        summaries = [
            "Urgent call - outdoor break",
            "Important phone call outside office",
            "Priority call with fresh air break",
            "Emergency call - stepping outside"
        ]
        return random_choice(summaries)
