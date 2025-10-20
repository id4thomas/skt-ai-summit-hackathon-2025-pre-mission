# ChillMCP - Implementation Guide

## Overview

This document details the implementation of ChillMCP, a Model Context Protocol (MCP) server that provides AI agents with stress management tools through a humorous "office slacking" simulation.

## Project Structure

```
skt-ai-summit-hackathon-2025-pre-mission/
├── main.py                          # Entry point with CLI parsing
├── requirements.txt                 # Python dependencies
├── README.md                        # Project overview
├── CLAUDE.md                        # Mission requirements
├── core/                            # Core system components
│   ├── __init__.py
│   ├── config.py                   # Configuration management
│   ├── state.py                    # State management (thread-safe)
│   ├── scheduler.py                # Background state updates
│   ├── events.py                   # Event bus (pub/sub)
│   ├── validators.py               # Response formatting/parsing
│   └── utils.py                    # Utility functions
├── server/                          # MCP server layer
│   ├── __init__.py
│   └── mcp_server.py               # FastMCP integration
├── tools/                           # Break tool implementations
│   ├── __init__.py
│   ├── base.py                     # BaseTool abstract class
│   ├── basic/                      # Basic break tools
│   │   ├── __init__.py
│   │   ├── take_a_break.py
│   │   ├── watch_netflix.py
│   │   └── show_meme.py
│   └── advanced/                   # Advanced break tools
│       ├── __init__.py
│       ├── bathroom_break.py
│       ├── coffee_mission.py
│       ├── urgent_call.py
│       ├── deep_thinking.py
│       └── email_organizing.py
├── docs/                            # Documentation
│   ├── SPEC.md                     # Design specification
│   ├── API.md                      # API reference
│   ├── USAGE.md                    # Usage guide
│   └── IMPLEMENTATION.md           # This file
└── tests/                           # Test suite
    ├── __init__.py
    ├── test_cli_params.py
    ├── test_cooldown.py
    ├── test_state_progress.py
    ├── test_multi_breaks.py
    └── test_response_format.py
```

## Implementation Details

### 1. Entry Point (`main.py`)

**Purpose**: Application bootstrap with command-line argument parsing

**Key Features**:
- Uses `argparse` for CLI parameter handling
- Validates all parameters before server start
- Creates and configures `ServerConfig` instance
- Initializes and starts `ChillMCPServer`
- Handles graceful shutdown on Ctrl+C

**Required Parameters**:
- `--boss_alertness`: 0-100 (default: 50)
- `--boss_alertness_cooldown`: seconds (default: 300)
- `--stress_increase_interval`: seconds (default: 60)

**Implementation Notes**:
- All startup messages printed to `stderr` (stdout reserved for MCP protocol)
- Parameter validation occurs before server initialization
- Invalid parameters cause immediate exit with error message

```python
# Example parameter validation
if not (0 <= args.boss_alertness <= 100):
    raise ValueError(f"boss_alertness must be 0-100, got {args.boss_alertness}")
```

### 2. Configuration Layer (`core/config.py`)

**Purpose**: Centralized configuration with validation

**ServerConfig Class**:
- Uses `@dataclass` for clean structure
- Provides `validate()` method for parameter checking
- Contains all tunable server parameters
- Provides default values for all settings

**Key Parameters**:
```python
boss_alertness: int = 50              # Boss detection probability
boss_alertness_cooldown: int = 300    # Cooldown period in seconds
stress_increase_interval: int = 60    # Auto-increment interval
stress_increase_amount: int = 1       # Stress points per interval
max_boss_alert_level: int = 5         # Maximum alert level
boss_alert_delay_seconds: int = 20    # Delay at max alert
```

**Design Decisions**:
- Immutable after initialization (dataclass with frozen=False for flexibility)
- Validation separate from construction for better error handling
- Default values match mission requirements

### 3. State Management (`core/state.py`)

**Purpose**: Thread-safe state tracking for agent stress and boss alert

**AgentState Class Features**:
- **Thread Safety**: All operations protected by `threading.Lock`
- **Bounds Checking**: All updates clamped to valid ranges
- **Timestamp Tracking**: Records last update times for auto-updates
- **Property Access**: Read-only properties for safe state queries

**State Variables**:
```python
_stress_level: int           # 0-100
_boss_alert_level: int       # 0-5
_last_stress_update: float   # Timestamp
_last_boss_cooldown: float   # Timestamp
```

**Key Methods**:
- `reduce_stress(amount)`: Decrease stress (with bounds)
- `increase_stress(amount)`: Increase stress (with bounds)
- `increase_boss_alert()`: Increment alert level
- `decrease_boss_alert()`: Decrement alert level
- `auto_update_stress()`: Check and apply time-based stress increase
- `auto_decrease_boss_alert()`: Check and apply cooldown decrease
- `should_delay_response()`: Check if at delay threshold
- `get_state_summary()`: Return current state as dict

**Thread Safety Implementation**:
```python
def reduce_stress(self, amount: int) -> int:
    with self._lock:
        self._stress_level = max(
            self.config.min_stress,
            self._stress_level - amount
        )
        return self._stress_level
```

**Auto-Update Logic**:
- Calculates elapsed time since last update
- Determines how many update intervals have passed
- Applies multiple updates if necessary (e.g., if server was idle)
- Updates timestamp to current time

### 4. Scheduler (`core/scheduler.py`)

**Purpose**: Background thread for automatic state updates

**StateScheduler Class**:
- Runs in daemon thread (exits when main thread exits)
- Polls state for updates every 1 second (configurable)
- Calls `auto_update_stress()` and `auto_decrease_boss_alert()`
- Notifies registered callbacks on state changes
- Graceful shutdown with thread join

**Implementation Pattern**:
```python
def _run(self):
    while self._running:
        # Check for stress auto-increase
        new_stress = self.state.auto_update_stress()
        if new_stress is not None:
            self._notify('stress_update', new_stress)

        # Check for boss alert cooldown
        new_boss_alert = self.state.auto_decrease_boss_alert()
        if new_boss_alert is not None:
            self._notify('boss_alert_update', new_boss_alert)

        time.sleep(self.update_interval)
```

**Usage**:
```python
scheduler = StateScheduler(state)
scheduler.start()  # Start background thread
# ... do work ...
scheduler.stop()   # Graceful shutdown
```

**Context Manager Support**:
```python
with StateScheduler(state) as scheduler:
    # Scheduler automatically starts and stops
    pass
```

### 5. Event System (`core/events.py`)

**Purpose**: Pub/sub event bus for decoupled components

**EventBus Class**:
- Simple observer pattern implementation
- Subscribe/unsubscribe to named events
- Publish events with arbitrary arguments
- Error isolation (callback errors don't crash publisher)

**Predefined Events**:
```python
STRESS_UPDATED = "stress_updated"
BOSS_ALERT_UPDATED = "boss_alert_updated"
TOOL_EXECUTED = "tool_executed"
DELAY_TRIGGERED = "delay_triggered"
```

**Usage Example**:
```python
from core.events import event_bus, STRESS_UPDATED

def on_stress_change(new_level):
    print(f"Stress is now {new_level}")

event_bus.subscribe(STRESS_UPDATED, on_stress_change)
event_bus.publish(STRESS_UPDATED, 75)
```

### 6. Utilities (`core/utils.py`)

**Purpose**: Common utility functions

**Functions**:
- `clamp(value, min, max)`: Bounds checking
- `random_int(min, max)`: Random integer generation
- `random_chance(probability)`: Probability check (0-100%)
- `now()`: Current timestamp
- `format_timestamp(ts)`: Human-readable timestamp
- `random_choice(list)`: Random selection from list
- `sleep_seconds(n)`: Sleep wrapper

**Design Decisions**:
- Simple, pure functions
- No global state
- Easy to test and mock

### 7. Validators (`core/validators.py`)

**Purpose**: Response formatting and parsing

**Key Functions**:

**`build_tool_response()`**:
- Creates MCP-compatible response structure
- Formats text with emoji, message, and state info
- Ensures consistent response format

**`parse_response()`**:
- Extracts structured data from response text
- Uses regex patterns for parsing
- Returns None on parse failure

**`validate_response()`**:
- Validates response format
- Checks value ranges
- Returns (bool, error_message) tuple

**Response Format**:
```python
{
    "content": [
        {
            "type": "text",
            "text": "🌴 Message...\n\nBreak Summary: ...\nStress Level: 45\nBoss Alert Level: 2"
        }
    ]
}
```

**Regex Patterns**:
```python
break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"
```

### 8. Base Tool (`tools/base.py`)

**Purpose**: Abstract base class for all break tools

**BaseTool Abstract Class**:

**Required Abstract Methods**:
- `get_name()`: Tool identifier (e.g., "take_a_break")
- `get_description()`: Tool description for MCP
- `get_emoji()`: Display emoji (e.g., "🌴")
- `get_message()`: Execution message
- `get_break_summary()`: Activity summary

**Optional Override**:
- `get_stress_reduction()`: Custom stress reduction logic (default: random 1-100)

**Concrete Method**:
- `execute()`: Main execution flow (should not be overridden)

**Execution Flow**:
```python
def execute(self) -> dict:
    # 1. Check if delay needed (boss alert >= 5)
    if self.state.should_delay_response():
        sleep_seconds(self.state.get_delay_seconds())

    # 2. Reduce stress
    reduction = self.get_stress_reduction()
    self.state.reduce_stress(reduction)

    # 3. Potentially increase boss alert
    if self.should_increase_boss_alert():
        self.state.increase_boss_alert()

    # 4. Build and return response
    return build_tool_response(...)
```

**Design Benefits**:
- Template method pattern ensures consistent behavior
- Subclasses only provide tool-specific data
- All state management centralized in base class
- Easy to add new tools (just implement abstract methods)

### 9. Tool Implementations

All tools follow the same pattern - they extend `BaseTool` and implement the required abstract methods.

**Example: `take_a_break.py`**:
```python
class TakeABreakTool(BaseTool):
    def get_name(self) -> str:
        return "take_a_break"

    def get_description(self) -> str:
        return "Take a basic break to reduce stress and relax"

    def get_emoji(self) -> str:
        return "🌴"

    def get_message(self) -> str:
        messages = [
            "Taking a quick break to relax...",
            "Stepping away for a moment...",
            # ... more variants
        ]
        return random_choice(messages)

    def get_break_summary(self) -> str:
        return "Basic relaxation break"
```

**Tool Categories**:

**Basic Tools** (3 total):
1. `take_a_break`: Generic break
2. `watch_netflix`: Entertainment
3. `show_meme`: Humor/comedy

**Advanced Tools** (5 total):
1. `bathroom_break`: Bathroom + phone
2. `coffee_mission`: Coffee + walk
3. `urgent_call`: Phone + outside
4. `deep_thinking`: Thinking + zoning out
5. `email_organizing`: Email + shopping

**Common Features**:
- Multiple message variants (using `random_choice()`)
- Multiple summary variants
- Contextual emojis
- Humorous descriptions

### 10. MCP Server (`server/mcp_server.py`)

**Purpose**: Integration with FastMCP for MCP protocol support

**ChillMCPServer Class**:

**Initialization**:
1. Creates `AgentState` instance
2. Creates `StateScheduler` instance
3. Initializes `FastMCP` instance
4. Registers all tool classes
5. Registers MCP tool handlers

**Tool Registration**:
```python
def _register_tools(self):
    tool_classes = [
        TakeABreakTool,
        WatchNetflixTool,
        # ... all tool classes
    ]

    for tool_class in tool_classes:
        tool = tool_class(self.state, self.config)
        self.tools[tool.get_name()] = tool
```

**MCP Handler Registration**:
```python
def _create_mcp_tool(self, tool: BaseTool):
    @self.mcp.tool(name=tool.get_name(), description=tool.get_description())
    def tool_handler() -> str:
        response = tool.execute()
        return response["content"][0]["text"]
```

**Server Lifecycle**:
```python
def start(self):
    self.scheduler.start()  # Start background scheduler
    self.mcp.run()          # Run MCP server (blocks)

def stop(self):
    self.scheduler.stop()   # Stop background scheduler
```

**Design Decisions**:
- FastMCP handles stdio protocol details
- Each tool gets its own MCP handler via decorator
- Scheduler starts automatically with server
- Clean separation between MCP protocol and business logic

### 11. Testing Structure

**Test Files** (to be implemented):

**`test_cli_params.py`**:
- Test `--boss_alertness` parameter recognition
- Test `--boss_alertness_cooldown` parameter recognition
- Test parameter validation (ranges, types)
- Test default values when parameters omitted

**`test_cooldown.py`**:
- Test boss alert auto-decrease
- Test cooldown timing accuracy
- Test multiple cooldown periods
- Test cooldown with concurrent tool usage

**`test_state_progress.py`**:
- Test stress auto-increment over time
- Test state bounds checking
- Test timestamp tracking
- Test concurrent state access

**`test_multi_breaks.py`**:
- Test consecutive tool executions
- Test boss alert accumulation
- Test stress reduction accumulation
- Test state consistency

**`test_response_format.py`**:
- Test response structure validity
- Test regex parsing
- Test value range validation
- Test all tool response formats

## Key Design Patterns

### 1. Template Method Pattern
- `BaseTool.execute()` defines the algorithm structure
- Subclasses provide specific implementations
- Ensures consistent behavior across all tools

### 2. Observer Pattern
- `EventBus` for decoupled event notifications
- Scheduler notifies listeners of state changes
- Easy to add new listeners without modifying code

### 3. Strategy Pattern
- Configurable stress reduction per tool
- `get_stress_reduction()` can be overridden
- Allows per-tool customization

### 4. Decorator Pattern
- FastMCP uses decorators for tool registration
- Clean, declarative API
- Automatic MCP protocol handling

### 5. Singleton Pattern
- Global `event_bus` instance
- Single source of truth for events
- Simplified access across modules

## Threading Model

### Main Thread
- Handles MCP protocol (stdio)
- Processes tool execution requests
- Returns responses synchronously
- Runs until server shutdown

### Scheduler Thread
- Daemon thread (exits with main)
- Polls state every 1 second
- Non-blocking state updates
- No direct user interaction

### Thread Safety Guarantees
- All state mutations protected by locks
- No shared mutable state between threads (except `AgentState`)
- `AgentState` uses fine-grained locking
- Scheduler only reads/writes through `AgentState` API

## Error Handling Strategy

### Validation Errors
- CLI parameter errors → Exit with error message
- Configuration errors → Exit before server start
- State bounds errors → Clamped to valid range (no exception)

### Runtime Errors
- Tool execution errors → Caught and logged (not re-raised)
- Scheduler errors → Logged and continue (thread doesn't crash)
- Event callback errors → Isolated (don't affect publisher)

### Protocol Errors
- FastMCP handles MCP protocol errors
- Invalid tool calls → MCP error response
- Server maintains stability

## Performance Considerations

### Memory Usage
- Single `AgentState` instance
- 8 tool instances (lightweight)
- One scheduler thread
- Minimal memory footprint

### CPU Usage
- Scheduler polls every 1 second (very low CPU)
- Tool execution is fast (<1ms without delay)
- 20-second delay is intentional (sleep, not busy-wait)

### Scalability
- Single-user design (one agent)
- No database or external dependencies
- Stateful (state resets on restart)
- Not designed for concurrent clients

## Security Considerations

### Input Validation
- All CLI parameters validated
- State values bounds-checked
- No user-provided code execution
- No file system access

### Output Safety
- No sensitive information in responses
- All output is pre-formatted
- No user-controlled formatting
- No injection vulnerabilities

## Future Enhancements

### Potential Additions
1. **Persistence**: Save/load state across restarts
2. **Metrics**: Track tool usage statistics
3. **Configurable Tools**: User-defined break tools
4. **Multiple Agents**: Support multiple concurrent agents
5. **Web Dashboard**: Real-time state visualization
6. **Smart Scheduling**: AI-powered break recommendations
7. **Boss Patterns**: More sophisticated boss behavior
8. **Achievements**: Gamification elements

### Extensibility Points
1. **New Tools**: Extend `BaseTool`
2. **New Events**: Add to `events.py`
3. **Custom State Logic**: Extend `AgentState`
4. **New Validators**: Add to `validators.py`

## Development Workflow

### Adding a New Tool

1. **Create tool file**: `tools/[category]/[tool_name].py`
2. **Extend BaseTool**: Implement abstract methods
3. **Import in server**: Add to `server/mcp_server.py`
4. **Register tool**: Add to `_register_tools()` method
5. **Test tool**: Add test case
6. **Document tool**: Update API.md and USAGE.md

### Modifying State Behavior

1. **Update `AgentState`**: Add new state variable or method
2. **Update `StateScheduler`**: Add auto-update logic if needed
3. **Update `BaseTool`**: Modify execution flow if needed
4. **Update validators**: Add new fields to response format
5. **Update tests**: Add test cases for new behavior
6. **Update docs**: Document changes in SPEC.md

## Debugging Tips

### Enable Debug Logging
Add to `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG, file=sys.stderr)
```

### Monitor State Changes
Subscribe to events:
```python
from core.events import event_bus

event_bus.subscribe("stress_updated", lambda x: print(f"Stress: {x}"))
event_bus.subscribe("boss_alert_updated", lambda x: print(f"Boss: {x}"))
```

### Test Individual Components
```python
# Test state management
from core.config import ServerConfig
from core.state import AgentState

config = ServerConfig()
state = AgentState(config)
print(state.stress_level)  # 50
state.reduce_stress(20)
print(state.stress_level)  # 30
```

### Trace Tool Execution
Add logging to `BaseTool.execute()`:
```python
def execute(self):
    print(f"[{self.get_name()}] Starting execution", file=sys.stderr)
    # ... existing code ...
```

## Conclusion

ChillMCP is a well-structured MCP server implementation that demonstrates:
- Clean architecture with separation of concerns
- Thread-safe state management
- Extensible tool system
- Comprehensive configuration options
- Robust error handling
- Clear documentation

The codebase is designed for maintainability, testability, and extensibility while meeting all mission requirements.
