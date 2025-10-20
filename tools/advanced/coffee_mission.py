"""
Advanced tool: coffee_mission
Pretend to get coffee and walk around the office.
"""

from tools.base import BaseTool
from core.utils import random_choice


class CoffeeMissionTool(BaseTool):
    """Coffee mission - excuse to walk around office."""

    def get_name(self) -> str:
        return "coffee_mission"

    def get_description(self) -> str:
        return "Go get coffee as an excuse to walk around and relax"

    def get_emoji(self) -> str:
        return "☕"

    def get_message(self) -> str:
        messages = [
            "Coffee time! Taking a leisurely stroll to the break room... ☕",
            "Need caffeine! Walking the long route to the coffee machine...",
            "Coffee mission initiated! Stopping to chat with everyone...",
            "Getting coffee... and maybe a snack... and a chat...",
            "Caffeine quest! Exploring every corner of the office..."
        ]
        return random_choice(messages)

    def get_break_summary(self) -> str:
        summaries = [
            "Coffee break with office tour",
            "Caffeine mission - extended walking break",
            "Coffee retrieval with social networking",
            "Break room expedition with coffee"
        ]
        return random_choice(summaries)
