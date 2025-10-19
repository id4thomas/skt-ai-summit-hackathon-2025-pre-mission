"""
Test state progression and bounds.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from chillmcp.core import OfficeState


async def test_stress_bounds():
    """Test that stress level respects bounds (0-100)"""
    print("Testing stress level bounds...")
    state = OfficeState(boss_alertness=50, boss_alertness_cooldown=60)

    # Test lower bound
    await state.update_stress(-1000)
    current = await state.get_state()
    assert current["stress_level"] == 0, f"Expected 0, got {current['stress_level']}"

    # Test upper bound
    await state.update_stress(1000)
    current = await state.get_state()
    assert current["stress_level"] == 100, f"Expected 100, got {current['stress_level']}"

    print("  ✓ Stress bounds test passed")


async def test_boss_alert_bounds():
    """Test that boss alert level respects bounds (0-5)"""
    print("Testing boss alert level bounds...")
    state = OfficeState(boss_alertness=50, boss_alertness_cooldown=60)

    # Test lower bound
    await state.update_boss_alert(-100)
    current = await state.get_state()
    assert current["boss_alert_level"] == 0, f"Expected 0, got {current['boss_alert_level']}"

    # Test upper bound
    await state.update_boss_alert(100)
    current = await state.get_state()
    assert current["boss_alert_level"] == 5, f"Expected 5, got {current['boss_alert_level']}"

    print("  ✓ Boss alert bounds test passed")


async def test_state_changes():
    """Test basic state changes"""
    print("Testing state changes...")
    state = OfficeState(boss_alertness=50, boss_alertness_cooldown=60)

    initial = await state.get_state()
    assert initial["stress_level"] == 50
    assert initial["boss_alert_level"] == 0

    # Decrease stress
    await state.update_stress(-10)
    current = await state.get_state()
    assert current["stress_level"] == 40

    # Increase boss alert
    await state.update_boss_alert(2)
    current = await state.get_state()
    assert current["boss_alert_level"] == 2

    print("  ✓ State changes test passed")


def main():
    print("Running state progression tests...\n")
    asyncio.run(test_stress_bounds())
    asyncio.run(test_boss_alert_bounds())
    asyncio.run(test_state_changes())
    print("\n✓ All state progression tests passed!")


if __name__ == "__main__":
    main()
