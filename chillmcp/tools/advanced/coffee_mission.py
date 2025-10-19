"""
Coffee mission tool.
"""

from ..base import BaseTool


class CoffeeMissionTool(BaseTool):
    """Coffee mission - good stress reduction, moderate risk"""

    def __init__(self):
        super().__init__(
            name="Going on a coffee mission",
            stress_reduction_range=(15, 30),
            boss_increase_chance=0.35
        )
