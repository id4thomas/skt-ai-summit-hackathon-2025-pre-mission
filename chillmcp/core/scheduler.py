"""
Background scheduler for automatic state updates.
"""

import asyncio
from .config import (
    STRESS_INCREASE_INTERVAL,
    STRESS_INCREASE_AMOUNT,
    BOSS_CAUGHT_DELAY
)
from .state import OfficeState


async def stress_increase_loop(state: OfficeState):
    """
    Periodically increase stress if no break is taken.

    Runs every STRESS_INCREASE_INTERVAL seconds and checks if
    a break was taken. If not, increases stress by STRESS_INCREASE_AMOUNT.

    Args:
        state: The OfficeState instance to update
    """
    while True:
        await asyncio.sleep(STRESS_INCREASE_INTERVAL)

        time_since_break = await state.get_time_since_last_break()
        if time_since_break >= STRESS_INCREASE_INTERVAL:
            await state.update_stress(STRESS_INCREASE_AMOUNT)


async def boss_alert_decrease_loop(state: OfficeState):
    """
    Periodically decrease boss alert level based on cooldown period.

    Runs every state.boss_alertness_cooldown seconds and decreases
    boss_alert_level by 1.

    Args:
        state: The OfficeState instance to update
    """
    while True:
        await asyncio.sleep(state.boss_alertness_cooldown)
        await state.update_boss_alert(-1)


async def check_boss_and_delay(state: OfficeState):
    """
    Check if boss is watching (level 5) and apply delay if needed.

    If boss_alert_level == 5, applies a BOSS_CAUGHT_DELAY second delay
    to simulate being caught by the boss.

    Args:
        state: The OfficeState instance to check
    """
    current_state = await state.get_state()
    if current_state["boss_alert_level"] == 5:
        # Boss caught you! Apply delay
        await asyncio.sleep(BOSS_CAUGHT_DELAY)


async def start_background_tasks(state: OfficeState):
    """
    Start all background monitoring tasks.

    Args:
        state: The OfficeState instance to monitor
    """
    asyncio.create_task(stress_increase_loop(state))
    asyncio.create_task(boss_alert_decrease_loop(state))
