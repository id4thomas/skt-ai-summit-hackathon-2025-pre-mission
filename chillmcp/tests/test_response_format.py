"""
Test response format validation.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from chillmcp.core import validate_response, format_response


def test_valid_response():
    """Test that valid responses pass validation"""
    response = format_response("Taking a break", 45, 2)
    result = validate_response(response)

    assert result["valid"] is True
    assert result["stress_level"] == 45
    assert result["boss_alert_level"] == 2
    assert result["break_summary"] == "Taking a break"
    assert len(result["errors"]) == 0
    print("✓ Valid response test passed")


def test_stress_out_of_range():
    """Test that stress level out of range fails validation"""
    response = "💬 Break Summary: Test\nStress Level: 150\nBoss Alert Level: 2"
    result = validate_response(response)

    assert result["valid"] is False
    assert any("out of range" in err for err in result["errors"])
    print("✓ Stress out of range test passed")


def test_boss_out_of_range():
    """Test that boss alert level out of range fails validation"""
    response = "💬 Break Summary: Test\nStress Level: 50\nBoss Alert Level: 10"
    result = validate_response(response)

    assert result["valid"] is False
    assert any("out of range" in err for err in result["errors"])
    print("✓ Boss out of range test passed")


def test_missing_fields():
    """Test that missing fields fail validation"""
    response = "Just some random text"
    result = validate_response(response)

    assert result["valid"] is False
    assert len(result["errors"]) == 3  # All three fields missing
    print("✓ Missing fields test passed")


if __name__ == "__main__":
    print("Running response format tests...\n")
    test_valid_response()
    test_stress_out_of_range()
    test_boss_out_of_range()
    test_missing_fields()
    print("\n✓ All response format tests passed!")
