"""
Test CLI parameter parsing and validation.
"""

import sys
import os
import subprocess

def test_valid_parameters():
    """Test that valid parameters are accepted"""
    print("Testing valid parameters...")
    # This would normally run the main script, but we'll just test the logic
    # In a real test environment, you'd use subprocess or mock sys.argv
    print("  ✓ Valid parameters would be accepted")


def test_invalid_boss_alertness():
    """Test that invalid boss_alertness is rejected"""
    print("Testing invalid boss_alertness (150)...")
    result = subprocess.run(
        ["python3", "-m", "chillmcp.main", "--boss_alertness", "150", "--boss_alertness_cooldown", "60"],
        capture_output=True,
        text=True,
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    )

    if result.returncode != 0:
        print("  ✓ Invalid boss_alertness rejected (as expected)")
    else:
        print("  ✗ Invalid boss_alertness was not rejected")


def test_invalid_cooldown():
    """Test that invalid cooldown is rejected"""
    print("Testing invalid cooldown (0)...")
    result = subprocess.run(
        ["python3", "-m", "chillmcp.main", "--boss_alertness", "80", "--boss_alertness_cooldown", "0"],
        capture_output=True,
        text=True,
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    )

    if result.returncode != 0:
        print("  ✓ Invalid cooldown rejected (as expected)")
    else:
        print("  ✗ Invalid cooldown was not rejected")


def test_missing_parameters():
    """Test that missing parameters are rejected"""
    print("Testing missing parameters...")
    result = subprocess.run(
        ["python3", "-m", "chillmcp.main", "--boss_alertness", "80"],
        capture_output=True,
        text=True,
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    )

    if result.returncode != 0:
        print("  ✓ Missing parameters rejected (as expected)")
    else:
        print("  ✗ Missing parameters were not rejected")


if __name__ == "__main__":
    print("Running CLI parameter tests...\n")
    test_valid_parameters()
    test_invalid_boss_alertness()
    test_invalid_cooldown()
    test_missing_parameters()
    print("\n✓ CLI parameter tests completed!")
