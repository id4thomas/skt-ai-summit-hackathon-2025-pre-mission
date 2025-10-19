"""
Test multiple break executions.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from chillmcp.core import OfficeState, validate_response
from chillmcp.tools import TakeABreakTool, WatchNetflixTool


async def test_multiple_breaks():
    """Test executing multiple breaks in sequence"""
    print("Testing multiple breaks...")
    state = OfficeState(boss_alertness=50, boss_alertness_cooldown=60)

    tool = TakeABreakTool()

    # Take 5 breaks
    for i in range(5):
        response = await tool.execute(state)
        result = validate_response(response)

        assert result["valid"], f"Break {i+1} produced invalid response: {result['errors']}"
        assert 0 <= result["stress_level"] <= 100
        assert 0 <= result["boss_alert_level"] <= 5

    print("  ✓ Multiple breaks test passed")


async def test_different_tools():
    """Test executing different break tools"""
    print("Testing different tools...")
    state = OfficeState(boss_alertness=50, boss_alertness_cooldown=60)

    tools = [
        TakeABreakTool(),
        WatchNetflixTool(),
    ]

    for tool in tools:
        response = await tool.execute(state)
        result = validate_response(response)

        assert result["valid"], f"Tool {tool.name} produced invalid response: {result['errors']}"

    print("  ✓ Different tools test passed")


async def test_stress_accumulation():
    """Test that stress can accumulate and be reduced"""
    print("Testing stress accumulation...")
    state = OfficeState(boss_alertness=50, boss_alertness_cooldown=60)

    # Increase stress manually
    await state.update_stress(30)
    current = await state.get_state()
    assert current["stress_level"] == 80

    # Take breaks to reduce stress
    tool = TakeABreakTool()
    for _ in range(3):
        await tool.execute(state)

    final = await state.get_state()
    assert final["stress_level"] < 80, "Stress should have decreased"

    print("  ✓ Stress accumulation test passed")


def main():
    print("Running multiple breaks tests...\n")
    asyncio.run(test_multiple_breaks())
    asyncio.run(test_different_tools())
    asyncio.run(test_stress_accumulation())
    print("\n✓ All multiple breaks tests passed!")


if __name__ == "__main__":
    main()
