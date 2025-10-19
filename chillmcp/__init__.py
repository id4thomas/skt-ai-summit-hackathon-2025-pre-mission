"""
ChillMCP - Office Break Simulator MCP Server
"""

__version__ = "1.0.0"
__author__ = "ChillMCP Team"
__description__ = "FastMCP-based office break simulator with stress and boss alertness management"

from .core import OfficeState
from .server import create_mcp_server
from .cli import parse_args

__all__ = [
    'OfficeState',
    'create_mcp_server',
    'parse_args',
]
