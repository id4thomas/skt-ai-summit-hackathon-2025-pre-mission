#!/usr/bin/env python3
"""
ChillMCP - Office Break Simulator MCP Server

Main entry point for the MCP server.
"""

import asyncio
from contextlib import asynccontextmanager
from .cli import parse_args
from .core import OfficeState, start_background_tasks
from .server import create_mcp_server


@asynccontextmanager
async def lifespan(state: OfficeState):
    """
    Lifespan context manager for background tasks.

    Args:
        state: The OfficeState instance
    """
    # Start background tasks
    task = asyncio.create_task(start_background_tasks(state))

    try:
        yield state
    finally:
        # Cancel background tasks on shutdown
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


def main():
    """Main entry point"""
    # Parse CLI arguments
    args = parse_args()

    # Initialize office state
    state = OfficeState(
        boss_alertness=args.boss_alertness,
        boss_alertness_cooldown=args.boss_alertness_cooldown
    )

    # Create MCP server with lifespan
    mcp = create_mcp_server(state, lambda _: lifespan(state))

    # Run the MCP server (stdio communication)
    mcp.run()


if __name__ == "__main__":
    main()
