"""
Advanced tool: deep_thinking
Pretend to be deep in thought while zoning out.
"""

from tools.base import BaseTool
from core.utils import random_choice


class DeepThinkingTool(BaseTool):
    """Deep thinking mode - actually just zoning out."""

    def get_name(self) -> str:
        return "deep_thinking"

    def get_description(self) -> str:
        return "Pretend to be deep in thought while actually zoning out"

    def get_emoji(self) -> str:
        return "🤔"

    def get_message(self) -> str:
        messages = [
            "Deep in thought... (actually spacing out completely) 🤔",
            "Contemplating complex problems... (mind completely blank)",
            "Strategic thinking session... (daydreaming about vacation)",
            "Analyzing architecture... (thinking about what's for lunch)",
            "Planning next steps... (absolutely nothing happening up here)"
        ]
        return random_choice(messages)

    def get_break_summary(self) -> str:
        summaries = [
            "Deep thinking session - strategic zoning out",
            "Contemplative break - mental vacation",
            "Thoughtful pause - daydreaming mode",
            "Strategic thinking time - mind wandering"
        ]
        return random_choice(summaries)
