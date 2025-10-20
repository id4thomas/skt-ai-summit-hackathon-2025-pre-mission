"""
Base tool class for ChillMCP server.
Provides common functionality for all break tools.
"""

from abc import ABC, abstractmethod
from typing import Optional

from core.config import ServerConfig
from core.state import AgentState
from core.utils import random_int, random_chance, sleep_seconds
from core.validators import build_tool_response, format_delay_warning


class BaseTool(ABC):
    """Base class for all ChillMCP tools."""

    def __init__(self, state: AgentState, config: ServerConfig):
        """
        Initialize tool.

        Args:
            state: AgentState instance
            config: ServerConfig instance
        """
        self.state = state
        self.config = config

    @abstractmethod
    def get_name(self) -> str:
        """Get tool name."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get tool description."""
        pass

    @abstractmethod
    def get_emoji(self) -> str:
        """Get tool emoji."""
        pass

    @abstractmethod
    def get_message(self) -> str:
        """Get tool message."""
        pass

    @abstractmethod
    def get_break_summary(self) -> str:
        """Get break activity summary."""
        pass

    def get_stress_reduction(self) -> int:
        """
        Calculate stress reduction for this break.
        Override in subclass for custom stress reduction logic.

        Returns:
            Stress reduction amount
        """
        return random_int(
            self.config.min_stress_reduction,
            self.config.max_stress_reduction
        )

    def should_increase_boss_alert(self) -> bool:
        """
        Determine if boss alert should increase.

        Returns:
            True if boss alert should increase
        """
        return random_chance(self.config.boss_alertness)

    def execute(self) -> dict:
        """
        Execute the tool and return MCP response.

        Returns:
            MCP-compatible response dictionary
        """
        # Check if we need to delay due to boss suspicion
        if self.state.should_delay_response():
            delay_seconds = self.state.get_delay_seconds()
            warning = format_delay_warning(delay_seconds)
            print(warning)  # Log warning
            sleep_seconds(delay_seconds)

        # Reduce stress
        stress_reduction = self.get_stress_reduction()
        self.state.reduce_stress(stress_reduction)

        # Potentially increase boss alert
        if self.should_increase_boss_alert():
            self.state.increase_boss_alert()

        # Get current state
        current_stress = self.state.stress_level
        current_boss_alert = self.state.boss_alert_level

        # Build response
        return build_tool_response(
            emoji=self.get_emoji(),
            message=self.get_message(),
            break_summary=self.get_break_summary(),
            stress_level=current_stress,
            boss_alert_level=current_boss_alert
        )
