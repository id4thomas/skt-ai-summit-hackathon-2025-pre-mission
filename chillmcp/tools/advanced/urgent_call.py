"""
Urgent call tool.
"""

from ..base import BaseTool


class UrgentCallTool(BaseTool):
    """Urgent personal call - moderate stress reduction, high risk"""

    def __init__(self):
        super().__init__(
            name="Taking an urgent personal call",
            stress_reduction_range=(12, 25),
            boss_increase_chance=0.45
        )
