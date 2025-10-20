"""
Basic break tool: watch_netflix
Watch Netflix for stress relief.
"""

from tools.base import BaseTool
from core.utils import random_choice


class WatchNetflixTool(BaseTool):
    """Watch Netflix to relax and unwind."""

    def get_name(self) -> str:
        return "watch_netflix"

    def get_description(self) -> str:
        return "Watch Netflix to reduce stress and enjoy entertainment"

    def get_emoji(self) -> str:
        return "📺"

    def get_message(self) -> str:
        shows = [
            "Binging the latest K-drama...",
            "Catching up on my favorite series...",
            "Netflix and chill mode activated...",
            "Watching an episode (or three)...",
            "Getting lost in a good show..."
        ]
        return random_choice(shows)

    def get_break_summary(self) -> str:
        summaries = [
            "Netflix break - watching series",
            "Entertainment break - streaming content",
            "Netflix chill time",
            "Video streaming break"
        ]
        return random_choice(summaries)
