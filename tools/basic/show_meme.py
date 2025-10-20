"""
Basic break tool: show_meme
Look at memes to reduce stress.
"""

from tools.base import BaseTool
from core.utils import random_choice


class ShowMemeTool(BaseTool):
    """Look at memes for stress relief."""

    def get_name(self) -> str:
        return "show_meme"

    def get_description(self) -> str:
        return "Look at funny memes to boost mood and reduce stress"

    def get_emoji(self) -> str:
        return "😂"

    def get_message(self) -> str:
        messages = [
            "Scrolling through hilarious memes...",
            "Looking at the dankest memes...",
            "Meme therapy in session...",
            "Browsing fresh memes for a quick laugh...",
            "Getting my daily dose of meme culture..."
        ]
        return random_choice(messages)

    def get_break_summary(self) -> str:
        summaries = [
            "Meme browsing break",
            "Comedy break - viewing memes",
            "Meme therapy session",
            "Humor break with internet memes"
        ]
        return random_choice(summaries)
