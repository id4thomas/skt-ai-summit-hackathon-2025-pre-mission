"""
FastMCP server adapter for ChillMCP.
"""

from fastmcp import FastMCP
from ..core import OfficeState, format_response
from ..tools import (
    TakeABreakTool,
    WatchNetflixTool,
    ShowMemeTool,
    BathroomBreakTool,
    CoffeeMissionTool,
    UrgentCallTool,
    DeepThinkingTool,
    EmailOrganizingTool
)


def create_mcp_server(state: OfficeState, lifespan=None) -> FastMCP:
    """
    Create and configure FastMCP server with all tools.

    Args:
        state: The OfficeState instance to use
        lifespan: Optional lifespan context manager for background tasks

    Returns:
        Configured FastMCP server instance
    """
    mcp = FastMCP("ChillMCP - Office Break Simulator", lifespan=lifespan)

    # Initialize all tools
    tools = {
        "take_a_break": TakeABreakTool(),
        "watch_netflix": WatchNetflixTool(),
        "show_meme": ShowMemeTool(),
        "bathroom_break": BathroomBreakTool(),
        "coffee_mission": CoffeeMissionTool(),
        "urgent_call": UrgentCallTool(),
        "deep_thinking": DeepThinkingTool(),
        "email_organizing": EmailOrganizingTool(),
    }

    # Register basic tools
    @mcp.tool()
    async def take_a_break() -> str:
        """Take a quick break to reduce stress"""
        return await tools["take_a_break"].execute(state)

    @mcp.tool()
    async def watch_netflix() -> str:
        """Watch Netflix to significantly reduce stress (but risky!)"""
        return await tools["watch_netflix"].execute(state)

    @mcp.tool()
    async def show_meme() -> str:
        """Look at memes for a quick laugh"""
        return await tools["show_meme"].execute(state)

    # Register advanced tools
    @mcp.tool()
    async def bathroom_break() -> str:
        """Take a bathroom break (low risk, moderate stress relief)"""
        return await tools["bathroom_break"].execute(state)

    @mcp.tool()
    async def coffee_mission() -> str:
        """Go on a coffee mission (good stress relief, moderate risk)"""
        return await tools["coffee_mission"].execute(state)

    @mcp.tool()
    async def urgent_call() -> str:
        """Take an 'urgent' personal call (moderate stress relief, higher risk)"""
        return await tools["urgent_call"].execute(state)

    @mcp.tool()
    async def deep_thinking() -> str:
        """Pretend to be in deep thought while actually relaxing (low risk)"""
        return await tools["deep_thinking"].execute(state)

    @mcp.tool()
    async def email_organizing() -> str:
        """Organize emails slowly while taking mental breaks (very low risk)"""
        return await tools["email_organizing"].execute(state)

    # Bonus tool: check status
    @mcp.tool()
    async def check_status() -> str:
        """Check current stress and boss alert levels"""
        current_state = await state.get_state()
        return format_response(
            "Checking current status",
            current_state["stress_level"],
            current_state["boss_alert_level"]
        )

    return mcp
