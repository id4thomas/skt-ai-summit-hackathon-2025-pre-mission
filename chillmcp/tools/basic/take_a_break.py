"""
Take a quick break tool.
"""

from ..base import BaseTool


class TakeABreakTool(BaseTool):
    """Quick break - low stress reduction, low risk"""

    def __init__(self):
        super().__init__(
            name="Taking a quick break",
            stress_reduction_range=(5, 15),
            boss_increase_chance=0.2
        )
