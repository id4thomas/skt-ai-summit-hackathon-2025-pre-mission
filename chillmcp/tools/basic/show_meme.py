"""
Show meme tool.
"""

from ..base import BaseTool


class ShowMemeTool(BaseTool):
    """Look at memes - moderate stress reduction, moderate risk"""

    def __init__(self):
        super().__init__(
            name="Looking at memes",
            stress_reduction_range=(8, 18),
            boss_increase_chance=0.3
        )
