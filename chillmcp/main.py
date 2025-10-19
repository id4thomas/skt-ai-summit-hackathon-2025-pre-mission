#!/usr/bin/env python3
"""
ChillMCP - Office Break Simulator MCP Server

Main entry point for the MCP server.
"""

import asyncio
from .cli import parse_args
from .core import OfficeState, start_background_tasks
from .server import create_mcp_server


def main():
    """Main entry point"""
    # Parse CLI arguments
    args = parse_args()

    # Initialize office state
    state = OfficeState(
        boss_alertness=args.boss_alertness,
        boss_alertness_cooldown=args.boss_alertness_cooldown
    )

    # Create MCP server
    mcp = create_mcp_server(state)

    # Create event loop and start background tasks
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Schedule background monitoring tasks
    loop.create_task(start_background_tasks(state))

    # Run the MCP server (stdio communication)
    mcp.run()


if __name__ == "__main__":
    main()
