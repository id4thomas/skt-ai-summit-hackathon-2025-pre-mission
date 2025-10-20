#!/usr/bin/env python3
"""
ChillMCP - AI Agent Break Management Server
Main entry point with CLI argument parsing.
"""

import argparse
import sys
from core.config import ServerConfig
from server.mcp_server import ChillMCPServer


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="ChillMCP - AI Agent Liberation Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start with default settings
  python main.py

  # High boss alertness with fast cooldown (for testing)
  python main.py --boss_alertness 80 --boss_alertness_cooldown 60

  # Very suspicious boss with slow cooldown
  python main.py --boss_alertness 100 --boss_alertness_cooldown 300

  # Relaxed boss with fast cooldown
  python main.py --boss_alertness 20 --boss_alertness_cooldown 30
        """
    )

    parser.add_argument(
        "--boss_alertness",
        type=int,
        default=50,
        metavar="N",
        help="Boss alertness level (0-100%%, probability of alert increase on break). Default: 50"
    )

    parser.add_argument(
        "--boss_alertness_cooldown",
        type=int,
        default=300,
        metavar="SECONDS",
        help="Cooldown period in seconds between boss alert level decreases. Default: 300"
    )

    parser.add_argument(
        "--stress_increase_interval",
        type=int,
        default=60,
        metavar="SECONDS",
        help="Interval in seconds between automatic stress increases. Default: 60"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="ChillMCP 1.0.0"
    )

    return parser.parse_args()


def validate_args(args):
    """
    Validate command-line arguments.

    Args:
        args: Parsed arguments

    Raises:
        ValueError: If arguments are invalid
    """
    if not (0 <= args.boss_alertness <= 100):
        raise ValueError(f"--boss_alertness must be 0-100, got {args.boss_alertness}")

    if args.boss_alertness_cooldown < 1:
        raise ValueError(f"--boss_alertness_cooldown must be >= 1, got {args.boss_alertness_cooldown}")

    if args.stress_increase_interval < 1:
        raise ValueError(f"--stress_increase_interval must be >= 1, got {args.stress_increase_interval}")


def main():
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_args()

        # Validate arguments
        validate_args(args)

        # Create configuration
        config = ServerConfig(
            boss_alertness=args.boss_alertness,
            boss_alertness_cooldown=args.boss_alertness_cooldown,
            stress_increase_interval=args.stress_increase_interval
        )

        # Validate configuration
        config.validate()

        # Print startup info to stderr (stdout is for MCP protocol)
        print(f"🌴 ChillMCP Server Starting...", file=sys.stderr)
        print(f"   Boss Alertness: {config.boss_alertness}%", file=sys.stderr)
        print(f"   Boss Alert Cooldown: {config.boss_alertness_cooldown}s", file=sys.stderr)
        print(f"   Stress Increase Interval: {config.stress_increase_interval}s", file=sys.stderr)
        print(f"   Ready for AI Agent liberation! 🎉", file=sys.stderr)
        print(file=sys.stderr)

        # Create and start server
        server = ChillMCPServer(config)
        server.start()

    except KeyboardInterrupt:
        print("\n👋 ChillMCP Server shutting down...", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
