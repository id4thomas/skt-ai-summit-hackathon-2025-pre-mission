# ChillMCP - Office Break Simulator

FastMCP-based MCP server that simulates office worker stress and boss alertness management.

## Overview

ChillMCP is a Model Context Protocol (MCP) server that helps manage stress levels and boss awareness in a simulated office environment. It provides various "break" tools that can reduce stress but might increase boss alertness.

## Features

- **Stress Management**: Track and reduce stress levels (0-100)
- **Boss Alertness**: Monitor boss attention level (0-5)
- **8 Break Tools**: From safe (email organizing) to risky (Netflix watching)
- **Automatic State Updates**: Stress increases over time, boss alertness decreases periodically
- **Consequence System**: Getting caught (level 5) results in 20-second delays

## Installation

### Prerequisites

- Python 3.11 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd skt-ai-summit-hackathon-2025-pre-mission
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

```bash
python main.py --boss_alertness 80 --boss_alertness_cooldown 60
```

**Parameters:**
- `--boss_alertness`: Boss attention level (0-100). Higher = more likely to notice breaks
- `--boss_alertness_cooldown`: Seconds between automatic boss alert decrease

**Examples:**

```bash
# Lenient boss, slow cooldown
python main.py --boss_alertness 30 --boss_alertness_cooldown 120

# Strict boss, fast cooldown
python main.py --boss_alertness 95 --boss_alertness_cooldown 30
```

### Connecting to MCP Clients

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "/path/to/main.py",
        "--boss_alertness",
        "80",
        "--boss_alertness_cooldown",
        "60"
      ]
    }
  }
}
```

## Available Tools

### Basic Tools

- **take_a_break**: Quick break (stress ↓5-15, risk 20%)
- **watch_netflix**: Netflix time (stress ↓20-40, risk 60%) ⚠️
- **show_meme**: Meme browsing (stress ↓8-18, risk 30%)

### Advanced Tools

- **bathroom_break**: Bathroom visit (stress ↓10-20, risk 10%) ✅
- **coffee_mission**: Coffee run (stress ↓15-30, risk 35%)
- **urgent_call**: Personal call (stress ↓12-25, risk 45%) ⚠️
- **deep_thinking**: Pretend thinking (stress ↓8-20, risk 15%)
- **email_organizing**: Slow email work (stress ↓5-12, risk 8%) ✅ (Safest)

### Status Tool

- **check_status**: View current stress and boss alert levels

## How It Works

### State Management

1. **Stress Level (0-100)**
   - Starts at 50
   - Decreases when taking breaks
   - Increases by 1 every minute without breaks

2. **Boss Alert Level (0-5)**
   - Starts at 0
   - May increase when taking breaks (probability depends on tool risk)
   - Decreases by 1 every cooldown period
   - At level 5: All actions delayed by 20 seconds (you're caught!)

### Response Format

All tools return responses in this format:

```
💬 Break Summary: <activity description>
Stress Level: <0-100>
Boss Alert Level: <0-5>
```

## Architecture

```
chillmcp/
├── core/               # Core logic
│   ├── config.py       # Configuration constants
│   ├── state.py        # State management
│   ├── scheduler.py    # Background tasks
│   ├── events.py       # Event pub/sub system
│   ├── validators.py   # Response validation
│   └── utils.py        # Utility functions
├── tools/              # Break tools
│   ├── base.py         # Base tool class
│   ├── basic/          # Basic break tools
│   └── advanced/       # Advanced break tools
├── server/             # MCP server
│   └── mcp_server.py   # FastMCP adapter
├── cli.py              # CLI argument parsing
└── main.py             # Entry point
```

## Testing

Run the test suite:

```bash
# Test response format validation
python3 chillmcp/tests/test_response_format.py

# Test state progression
python3 chillmcp/tests/test_state_progress.py

# Test multiple breaks
python3 chillmcp/tests/test_multi_breaks.py

# Test CLI parameters
python3 chillmcp/tests/test_cli_params.py
```

## Development

### Adding a New Break Tool

1. Create a new file in `chillmcp/tools/basic/` or `chillmcp/tools/advanced/`
2. Extend `BaseTool` class
3. Define name, stress reduction range, and boss increase chance
4. Register in `chillmcp/server/mcp_server.py`

Example:

```python
from ..base import BaseTool

class MyCustomBreakTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="My custom break",
            stress_reduction_range=(10, 25),
            boss_increase_chance=0.25
        )
```

## Documentation

- [SPEC.md](docs/SPEC.md): Design and specification
- [API.md](docs/API.md): Detailed API documentation
- [IMPLEMENTATION.md](../IMPLEMENTATION.md): Complete implementation guide

## License

SKT AI Summit Hackathon 2025 Pre-mission

## Credits

Built with [FastMCP](https://github.com/jlowin/fastmcp)
