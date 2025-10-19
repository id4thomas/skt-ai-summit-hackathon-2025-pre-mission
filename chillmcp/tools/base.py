"""
Base tool class and common break logic.
"""

import random
from typing import Tuple
from ..core import (
    OfficeState,
    format_response,
    check_boss_and_delay,
    rand
)


class BaseTool:
    """
    Base class for all break tools.

    Provides common logic for stress reduction, boss alert increase,
    and response formatting.
    """

    def __init__(
        self,
        name: str,
        stress_reduction_range: Tuple[int, int],
        boss_increase_chance: float
    ):
        """
        Initialize a break tool.

        Args:
            name: Name of the break activity
            stress_reduction_range: (min, max) stress reduction range
            boss_increase_chance: Probability (0.0-1.0) of boss alert increase
        """
        self.name = name
        self.stress_reduction_range = stress_reduction_range
        self.boss_increase_chance = boss_increase_chance

    async def execute(self, state: OfficeState) -> str:
        """
        Execute the break activity.

        Args:
            state: The OfficeState instance

        Returns:
            Formatted response string
        """
        # 1. Mark break taken (updates last_break_time)
        await state.mark_break_taken()

        # 2. Reduce stress (random amount)
        stress_reduction = rand(
            self.stress_reduction_range[0],
            self.stress_reduction_range[1]
        )
        await state.update_stress(-stress_reduction)

        # 3. Possibly increase boss alert level
        if random.random() < self.boss_increase_chance:
            # Boss alertness parameter affects increase probability
            if rand(0, 100) < state.boss_alertness:
                await state.update_boss_alert(1)

        # 4. Check if boss caught you (level 5) and apply delay
        await check_boss_and_delay(state)

        # 5. Get final state and return formatted response
        final_state = await state.get_state()

        return format_response(
            self.name,
            final_state["stress_level"],
            final_state["boss_alert_level"]
        )
