"""
Watch Netflix tool.
"""

from ..base import BaseTool


class WatchNetflixTool(BaseTool):
    """Watch Netflix - high stress reduction, high risk"""

    def __init__(self):
        super().__init__(
            name="Watching Netflix",
            stress_reduction_range=(20, 40),
            boss_increase_chance=0.6
        )
