"""
Bathroom break tool.
"""

from ..base import BaseTool


class BathroomBreakTool(BaseTool):
    """Bathroom break - moderate stress reduction, very low risk"""

    def __init__(self):
        super().__init__(
            name="Taking a bathroom break",
            stress_reduction_range=(10, 20),
            boss_increase_chance=0.1
        )
