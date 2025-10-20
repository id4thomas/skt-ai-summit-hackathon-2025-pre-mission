"""
Advanced tool: email_organizing
Pretend to organize emails while online shopping.
"""

from tools.base import BaseTool
from core.utils import random_choice


class EmailOrganizingTool(BaseTool):
    """Email organizing - actually online shopping."""

    def get_name(self) -> str:
        return "email_organizing"

    def get_description(self) -> str:
        return "Pretend to organize emails while browsing online shopping sites"

    def get_emoji(self) -> str:
        return "📧"

    def get_message(self) -> str:
        messages = [
            "Organizing inbox... (browsing online shopping) 🛒",
            "Managing emails... (adding items to cart)",
            "Cleaning up email... (checking out sales)",
            "Email maintenance... (window shopping online)",
            "Inbox organization... (hunting for deals)"
        ]
        return random_choice(messages)

    def get_break_summary(self) -> str:
        summaries = [
            "Email organization with online shopping",
            "Inbox management - e-commerce browsing",
            "Email cleanup - retail therapy",
            "Message organizing with shopping research"
        ]
        return random_choice(summaries)
