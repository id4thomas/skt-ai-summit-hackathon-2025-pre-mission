"""
MCP server adapter for ChillMCP.
Integrates with FastMCP to provide stdio-based MCP server.
"""

from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

from core.config import ServerConfig
from core.state import AgentState
from core.scheduler import StateScheduler
from tools.base import BaseTool

# Import all tool classes
from tools.basic.take_a_break import TakeABreakTool
from tools.basic.watch_netflix import WatchNetflixTool
from tools.basic.show_meme import ShowMemeTool
from tools.advanced.bathroom_break import BathroomBreakTool
from tools.advanced.coffee_mission import CoffeeMissionTool
from tools.advanced.urgent_call import UrgentCallTool
from tools.advanced.deep_thinking import DeepThinkingTool
from tools.advanced.email_organizing import EmailOrganizingTool


class ChillMCPServer:
    """ChillMCP server implementation using FastMCP."""

    def __init__(self, config: ServerConfig):
        """
        Initialize ChillMCP server.

        Args:
            config: Server configuration
        """
        self.config = config
        self.state = AgentState(config)
        self.scheduler = StateScheduler(self.state)

        # Initialize FastMCP
        self.mcp = FastMCP("ChillMCP")

        # Initialize tools
        self.tools: Dict[str, BaseTool] = {}
        self._register_tools()

        # Register MCP tool handlers
        self._register_mcp_tools()

    def _register_tools(self):
        """Register all available tools."""
        tool_classes = [
            TakeABreakTool,
            WatchNetflixTool,
            ShowMemeTool,
            BathroomBreakTool,
            CoffeeMissionTool,
            UrgentCallTool,
            DeepThinkingTool,
            EmailOrganizingTool
        ]

        for tool_class in tool_classes:
            tool = tool_class(self.state, self.config)
            self.tools[tool.get_name()] = tool

    def _register_mcp_tools(self):
        """Register tools with FastMCP."""
        # Register each tool with MCP
        for tool_name, tool in self.tools.items():
            self._create_mcp_tool(tool)

    def _create_mcp_tool(self, tool: BaseTool):
        """
        Create and register an MCP tool handler.

        Args:
            tool: Tool instance to register
        """
        @self.mcp.tool(name=tool.get_name(), description=tool.get_description())
        def tool_handler() -> str:
            """Execute the tool and return formatted response."""
            response = tool.execute()
            # Extract text from MCP response format
            return response["content"][0]["text"]

    def start(self):
        """Start the server and scheduler."""
        # Start background scheduler
        self.scheduler.start()

        # Run MCP server (blocks)
        self.mcp.run()

    def stop(self):
        """Stop the server and scheduler."""
        self.scheduler.stop()

    def get_server_info(self) -> Dict[str, Any]:
        """Get server information."""
        return {
            "name": "ChillMCP",
            "version": "1.0.0",
            "description": "AI Agent break management server",
            "tools": [tool.get_name() for tool in self.tools.values()],
            "config": {
                "boss_alertness": self.config.boss_alertness,
                "boss_alertness_cooldown": self.config.boss_alertness_cooldown,
                "stress_increase_interval": self.config.stress_increase_interval
            }
        }
