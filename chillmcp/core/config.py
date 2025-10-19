"""
Configuration constants and default values for ChillMCP.
"""

# Default values
DEFAULT_STRESS_LEVEL = 50
DEFAULT_BOSS_ALERT_LEVEL = 0

# Bounds
MIN_STRESS = 0
MAX_STRESS = 100
MIN_BOSS_ALERT = 0
MAX_BOSS_ALERT = 5

# Timings
STRESS_INCREASE_INTERVAL = 60  # seconds (1 minute)
STRESS_INCREASE_AMOUNT = 1

# Boss alert delay when caught (level 5)
BOSS_CAUGHT_DELAY = 20  # seconds

# CLI parameter bounds
MIN_BOSS_ALERTNESS = 0
MAX_BOSS_ALERTNESS = 100
MIN_COOLDOWN = 1  # seconds
