"""
Configuration module for ChillMCP server.
Defines default values and configuration parameters.
"""

from dataclasses import dataclass


@dataclass
class ServerConfig:
    """Server configuration with default values."""

    # Boss alertness settings
    boss_alertness: int = 50  # 0-100, probability of boss alert increase on break
    boss_alertness_cooldown: int = 300  # seconds between automatic boss alert decreases

    # Stress settings
    stress_increase_interval: int = 60  # seconds between automatic stress increases
    stress_increase_amount: int = 1  # stress points added per interval
    min_stress_reduction: int = 1  # minimum stress reduction per break
    max_stress_reduction: int = 100  # maximum stress reduction per break

    # Boss alert settings
    max_boss_alert_level: int = 5  # maximum boss alert level
    boss_alert_delay_threshold: int = 5  # level at which 20s delay occurs
    boss_alert_delay_seconds: int = 20  # delay duration when boss is suspicious

    # State limits
    min_stress: int = 0
    max_stress: int = 100
    min_boss_alert: int = 0
    max_boss_alert: int = 5

    def validate(self):
        """Validate configuration values."""
        if not (0 <= self.boss_alertness <= 100):
            raise ValueError(f"boss_alertness must be 0-100, got {self.boss_alertness}")

        if self.boss_alertness_cooldown < 1:
            raise ValueError(f"boss_alertness_cooldown must be >= 1, got {self.boss_alertness_cooldown}")

        if self.stress_increase_interval < 1:
            raise ValueError(f"stress_increase_interval must be >= 1, got {self.stress_increase_interval}")

        return True


# Default configuration instance
DEFAULT_CONFIG = ServerConfig()
