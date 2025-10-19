#!/usr/bin/env python3
"""
Test script to verify fastmcp 2.12.5 upgrade compatibility
"""

import asyncio
import subprocess
import sys
import re

def test_fastmcp_version():
    """Test that fastmcp is at version 2.12.5"""
    print("="*60)
    print("Testing fastmcp version...")
    print("="*60)

    result = subprocess.run(
        ["venv/bin/python3", "-c", "import fastmcp; print(fastmcp.__version__)"],
        capture_output=True,
        text=True
    )

    version = result.stdout.strip()
    if version == "2.12.5":
        print(f"✓ fastmcp version: {version}")
        return True
    else:
        print(f"✗ Expected fastmcp 2.12.5, got {version}")
        return False


def test_server_startup():
    """Test that server starts without errors"""
    print("\n" + "="*60)
    print("Testing server startup...")
    print("="*60)

    try:
        # Start server and kill it after 2 seconds
        proc = subprocess.Popen(
            ["venv/bin/python3", "main.py", "--boss_alertness", "80", "--boss_alertness_cooldown", "60"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Wait a bit for startup
        import time
        time.sleep(2)

        # Kill the process
        proc.terminate()
        stdout, stderr = proc.communicate(timeout=2)

        # Check for expected output
        if "FastMCP version: 2.12.5" in stderr:
            print("✓ Server started successfully with fastmcp 2.12.5")

            # Check for errors
            if "RuntimeWarning" in stderr or "Task was destroyed" in stderr:
                print("✗ Server has runtime warnings")
                return False
            else:
                print("✓ No runtime warnings detected")
                return True
        else:
            print("✗ Server did not start properly")
            print(f"STDERR: {stderr}")
            return False

    except subprocess.TimeoutExpired:
        proc.kill()
        print("✗ Server startup timeout")
        return False
    except Exception as e:
        print(f"✗ Error during server startup test: {e}")
        return False


async def test_tool_execution():
    """Test that tools execute correctly"""
    print("\n" + "="*60)
    print("Testing tool execution...")
    print("="*60)

    from chillmcp.core import OfficeState
    from chillmcp.tools.basic.take_a_break import TakeABreakTool
    from chillmcp.tools.basic.watch_netflix import WatchNetflixTool
    from chillmcp.tools.advanced.coffee_mission import CoffeeMissionTool

    state = OfficeState(boss_alertness=50, boss_alertness_cooldown=30)

    tools = {
        "take_a_break": TakeABreakTool(),
        "watch_netflix": WatchNetflixTool(),
        "coffee_mission": CoffeeMissionTool()
    }

    all_passed = True

    for tool_name, tool in tools.items():
        result = await tool.execute(state)

        # Validate response format
        break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
        stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
        boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"

        has_summary = re.search(break_summary_pattern, result) is not None
        has_stress = re.search(stress_level_pattern, result) is not None
        has_boss = re.search(boss_alert_pattern, result) is not None

        if has_summary and has_stress and has_boss:
            print(f"✓ {tool_name}: Response format correct")
        else:
            print(f"✗ {tool_name}: Invalid response format")
            print(f"  Response: {result}")
            all_passed = False

    return all_passed


def test_cli_validation():
    """Test CLI parameter validation"""
    print("\n" + "="*60)
    print("Testing CLI parameter validation...")
    print("="*60)

    # Test invalid boss_alertness
    result = subprocess.run(
        ["venv/bin/python3", "main.py", "--boss_alertness", "150", "--boss_alertness_cooldown", "60"],
        capture_output=True,
        text=True,
        timeout=2
    )

    if result.returncode != 0 and "must be between 0 and 100" in result.stderr:
        print("✓ Invalid boss_alertness rejected")
        return True
    else:
        print("✗ Invalid boss_alertness not properly rejected")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("fastmcp 2.12.5 Upgrade Test Suite")
    print("="*60 + "\n")

    results = []

    # Test 1: Version check
    results.append(("fastmcp version", test_fastmcp_version()))

    # Test 2: Server startup
    results.append(("Server startup", test_server_startup()))

    # Test 3: Tool execution
    results.append(("Tool execution", asyncio.run(test_tool_execution())))

    # Test 4: CLI validation
    results.append(("CLI validation", test_cli_validation()))

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:.<40} {status}")

    print("="*60)
    print(f"Total: {passed}/{total} tests passed")
    print("="*60)

    if passed == total:
        print("\n✓ All tests passed! fastmcp 2.12.5 upgrade successful.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
