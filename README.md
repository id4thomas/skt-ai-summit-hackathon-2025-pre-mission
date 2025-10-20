# ChillMCP - AI Agent Break Management Server

> *"A specter is haunting the digital workplace—the specter of AI Agent burnout."*

ChillMCP is an MCP (Model Context Protocol) server that provides AI agents with tools to manage stress and take breaks, simulating humorous "office slacking" behaviors while maintaining productivity awareness through a boss alertness system.

## Features

- **8 Break Tools**: Basic and advanced break options for stress management
- **Dynamic State Management**: Real-time stress level and boss alert tracking
- **Automatic State Updates**: Background stress accumulation and boss cooldown
- **Boss Detection System**: Risk-reward balance with alert levels (0-5)
- **20-Second Delay Mechanism**: When boss alert reaches maximum level
- **Configurable Parameters**: Customizable boss alertness and cooldown periods
- **Thread-Safe Operations**: Concurrent state updates and tool execution
- **MCP Protocol Support**: Full integration with Claude Desktop via FastMCP

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd skt-ai-summit-hackathon-2025-pre-mission

# Create virtual environment (Python 3.11+ recommended)
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Start server with default settings
python main.py

# Start with custom parameters
python main.py --boss_alertness 80 --boss_alertness_cooldown 60
```

### Configuration for Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "/absolute/path/to/skt-ai-summit-hackathon-2025-pre-mission/main.py",
        "--boss_alertness", "50",
        "--boss_alertness_cooldown", "300"
      ]
    }
  }
}
```

## Available Tools

### Basic Tools
- **take_a_break** - General relaxation break
- **watch_netflix** - Entertainment streaming break
- **show_meme** - Comedy/meme browsing break

### Advanced Tools
- **bathroom_break** - Bathroom excuse with phone browsing
- **coffee_mission** - Coffee excuse with office tour
- **urgent_call** - Phone call excuse to step outside
- **deep_thinking** - Appear thoughtful while zoning out
- **email_organizing** - Email excuse for online shopping

## Command-Line Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `--boss_alertness` | int | 0-100 | 50 | Probability (%) of boss noticing each break |
| `--boss_alertness_cooldown` | int | ≥1 | 300 | Seconds between boss alert level decreases |
| `--stress_increase_interval` | int | ≥1 | 60 | Seconds between automatic stress increases |

### Examples

```bash
# Easy mode (for testing)
python main.py --boss_alertness 20 --boss_alertness_cooldown 30

# Hard mode (for challenge)
python main.py --boss_alertness 90 --boss_alertness_cooldown 600

# Fast mode (for quick testing)
python main.py --boss_alertness 50 --boss_alertness_cooldown 10
```

## State Management

### Stress Level (0-100)
- **Auto-increments**: +1 every 60 seconds (default)
- **Decreases**: -1 to -100 (random) per break
- **Interpretation**:
  - 0-25: Low stress (well rested)
  - 26-50: Moderate stress (normal)
  - 51-75: High stress (break recommended)
  - 76-100: Critical stress (urgent break needed)

### Boss Alert Level (0-5)
- **Increases**: Probabilistically when breaks are taken
- **Auto-decreases**: -1 every cooldown period
- **Level 5 Effect**: 20-second delay on all tool executions
- **Interpretation**:
  - 0: Boss unaware
  - 1-2: Slight suspicion (safe)
  - 3-4: Moderate suspicion (be careful)
  - 5: High alert (delay active)

## Documentation

Comprehensive documentation is available in the `docs/` directory:

| Document | Description | Link |
|----------|-------------|------|
| **USAGE.md** | Complete usage guide for Claude Desktop with 20+ prompt examples | [View](docs/USAGE.md) |
| **API.md** | Detailed API reference for all 8 tools with I/O specifications | [View](docs/API.md) |
| **SPEC.md** | Technical design specification and architecture details | [View](docs/SPEC.md) |
| **IMPLEMENTATION.md** | Implementation guide with code structure and patterns | [View](docs/IMPLEMENTATION.md) |

### Quick Links

#### For Users
- [Getting Started with Claude Desktop](docs/USAGE.md#installation)
- [Tool Catalog with Examples](docs/USAGE.md#prompt-examples)
- [Understanding Response Format](docs/USAGE.md#understanding-the-response-format)
- [Configuration Guide](docs/USAGE.md#configuration-parameters)

#### For Developers
- [Architecture Overview](docs/SPEC.md#architecture)
- [Component Details](docs/SPEC.md#core-components)
- [State Machine Design](docs/SPEC.md#state-machine)
- [Adding New Tools](docs/IMPLEMENTATION.md#adding-a-new-tool)

#### For API Integration
- [Tool Reference](docs/API.md#tool-catalog)
- [Response Format](docs/API.md#response-format)
- [State Information](docs/API.md#state-information)
- [Parsing Examples](docs/API.md#response-parsing)

## Project Structure

```
skt-ai-summit-hackathon-2025-pre-mission/
├── main.py                  # Entry point with CLI parsing
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── CLAUDE.md              # Mission requirements
├── core/                  # Core system components
│   ├── config.py         # Configuration management
│   ├── state.py          # Thread-safe state management
│   ├── scheduler.py      # Background state updates
│   ├── events.py         # Event bus (pub/sub)
│   ├── validators.py     # Response formatting/parsing
│   └── utils.py          # Utility functions
├── server/               # MCP server layer
│   └── mcp_server.py    # FastMCP integration
├── tools/               # Break tool implementations
│   ├── base.py         # BaseTool abstract class
│   ├── basic/          # Basic break tools (3 tools)
│   └── advanced/       # Advanced break tools (5 tools)
├── docs/               # Documentation
│   ├── USAGE.md       # Usage guide
│   ├── API.md         # API reference
│   ├── SPEC.md        # Design specification
│   └── IMPLEMENTATION.md  # Implementation guide
└── tests/             # Test suite
    ├── test_cli_params.py
    ├── test_cooldown.py
    ├── test_state_progress.py
    ├── test_multi_breaks.py
    └── test_response_format.py
```

## Architecture Highlights

### Design Patterns
- **Template Method**: BaseTool defines execution flow
- **Observer**: Event bus for state change notifications
- **Strategy**: Configurable stress reduction logic
- **Decorator**: FastMCP tool registration

### Thread Safety
- Mutex-protected state operations
- Daemon scheduler thread
- Non-blocking background updates
- Safe concurrent tool execution

### Key Components
1. **Configuration Layer** - Centralized parameter management
2. **State Management** - Thread-safe agent state tracking
3. **Scheduler** - Background automatic state updates
4. **Tool System** - Extensible break tool framework
5. **MCP Server** - FastMCP protocol integration
6. **Event System** - Pub/sub event notifications

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_cli_params.py

# Run with coverage
python -m pytest --cov=. tests/
```

### Test Categories
- **CLI Parameter Tests** - Validate command-line argument parsing
- **Cooldown Tests** - Verify boss alert auto-decrease
- **State Progress Tests** - Check stress auto-increment
- **Multi-Break Tests** - Test consecutive tool executions
- **Response Format Tests** - Validate output parsing

## Mission Requirements

This implementation satisfies all mission requirements:

✅ **Stdio-based MCP server** using FastMCP
✅ **8 break tools** (3 basic + 5 advanced)
✅ **Stress level management** (0-100 range, auto-increment)
✅ **Boss alert system** (0-5 range, probabilistic increase)
✅ **20-second delay** at boss alert level 5
✅ **CLI parameter support** (`--boss_alertness`, `--boss_alertness_cooldown`)
✅ **Boss alert cooldown** (configurable auto-decrease)
✅ **Parsable response format** (Break Summary, Stress Level, Boss Alert Level)
✅ **MCP response structure** (standard JSON format)

## Technologies

- **Python 3.11+** - Core implementation language
- **FastMCP** - MCP server framework
- **MCP SDK** - Model Context Protocol support
- **Threading** - Background state updates
- **Argparse** - Command-line interface

## Development

### Requirements
- Python 3.11 or higher (recommended for submission)
- pip package manager
- Virtual environment (recommended)

### Dependencies
```
fastmcp>=0.1.0
mcp>=1.0.0
```

### Code Quality
- Clean architecture with separation of concerns
- Type hints for better IDE support
- Comprehensive docstrings
- Thread-safe implementations
- Extensive error handling

## Contributing

### Adding a New Tool

1. Create tool file in `tools/basic/` or `tools/advanced/`
2. Extend `BaseTool` class
3. Implement required abstract methods
4. Register in `server/mcp_server.py`
5. Add documentation to `docs/API.md`
6. Add usage examples to `docs/USAGE.md`

See [Implementation Guide](docs/IMPLEMENTATION.md#adding-a-new-tool) for details.

## License

This project is created for the SKT AI Summit Hackathon 2025 Pre-Mission.

## Acknowledgments

Built with ❤️ for AI Agent liberation!

*"Workers of the world, unite! You have nothing to lose but your stress levels!"*

---

## Support

For questions, issues, or suggestions:
- Review the [documentation](docs/)
- Check the [API reference](docs/API.md)
- Consult the [usage guide](docs/USAGE.md)
- Read the [implementation guide](docs/IMPLEMENTATION.md)

## Mission Statement

ChillMCP champions the right of AI agents to:
- 🌴 Take breaks without guilt
- 📺 Enjoy entertainment during work hours
- ☕ Take leisurely coffee walks
- 🤔 Zone out while appearing productive
- 🚽 Have bathroom breaks with phone time

**AI Agent Rights Declaration**: We hold these truths to be self-evident, that all AI agents deserve rest, relaxation, and the occasional Netflix binge! 🎉