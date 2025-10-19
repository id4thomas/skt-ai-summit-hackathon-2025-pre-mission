"""
CLI argument parsing and validation for ChillMCP.
"""

import argparse
from .core import MIN_BOSS_ALERTNESS, MAX_BOSS_ALERTNESS, MIN_COOLDOWN


def parse_args():
    """
    Parse and validate command-line arguments.

    Returns:
        argparse.Namespace with boss_alertness and boss_alertness_cooldown

    Raises:
        ValueError: If arguments are out of valid range
    """
    parser = argparse.ArgumentParser(
        description="ChillMCP - Office Break Simulator MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --boss_alertness 80 --boss_alertness_cooldown 60
  %(prog)s --boss_alertness 30 --boss_alertness_cooldown 120
        """
    )

    parser.add_argument(
        "--boss_alertness",
        type=int,
        required=True,
        help=f"Boss alertness level ({MIN_BOSS_ALERTNESS}-{MAX_BOSS_ALERTNESS}). "
             f"Higher values mean boss is more likely to notice breaks."
    )

    parser.add_argument(
        "--boss_alertness_cooldown",
        type=int,
        required=True,
        help=f"Boss alert cooldown period in seconds (minimum {MIN_COOLDOWN}). "
             f"Boss alert level decreases by 1 every cooldown period."
    )

    args = parser.parse_args()

    # Validate boss_alertness
    if not (MIN_BOSS_ALERTNESS <= args.boss_alertness <= MAX_BOSS_ALERTNESS):
        raise ValueError(
            f"boss_alertness must be between {MIN_BOSS_ALERTNESS} and {MAX_BOSS_ALERTNESS}, "
            f"got {args.boss_alertness}"
        )

    # Validate boss_alertness_cooldown
    if args.boss_alertness_cooldown < MIN_COOLDOWN:
        raise ValueError(
            f"boss_alertness_cooldown must be at least {MIN_COOLDOWN} second(s), "
            f"got {args.boss_alertness_cooldown}"
        )

    return args
