"""
Deep thinking tool.
"""

from ..base import BaseTool


class DeepThinkingTool(BaseTool):
    """Deep thinking (actually relaxing) - moderate stress reduction, low risk"""

    def __init__(self):
        super().__init__(
            name="Deep thinking (actually relaxing)",
            stress_reduction_range=(8, 20),
            boss_increase_chance=0.15
        )
