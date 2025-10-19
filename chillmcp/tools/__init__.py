"""
Tools module for ChillMCP.
"""

from .base import BaseTool
from .basic import TakeABreakTool, WatchNetflixTool, ShowMemeTool
from .advanced import (
    BathroomBreakTool,
    CoffeeMissionTool,
    UrgentCallTool,
    DeepThinkingTool,
    EmailOrganizingTool
)

__all__ = [
    'BaseTool',
    'TakeABreakTool',
    'WatchNetflixTool',
    'ShowMemeTool',
    'BathroomBreakTool',
    'CoffeeMissionTool',
    'UrgentCallTool',
    'DeepThinkingTool',
    'EmailOrganizingTool',
]
