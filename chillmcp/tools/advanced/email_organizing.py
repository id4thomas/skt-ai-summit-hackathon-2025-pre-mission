"""
Email organizing tool.
"""

from ..base import BaseTool


class EmailOrganizingTool(BaseTool):
    """Email organizing - low stress reduction, very low risk (safest option)"""

    def __init__(self):
        super().__init__(
            name="Organizing emails slowly",
            stress_reduction_range=(5, 12),
            boss_increase_chance=0.08
        )
