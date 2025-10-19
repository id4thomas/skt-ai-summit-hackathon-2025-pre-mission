# ChillMCP - Design Specification

## 1. System Overview

ChillMCP is a FastMCP-based Model Context Protocol server that simulates office worker behavior, managing two primary metrics:
- **Stress Level** (0-100): Worker's stress accumulation
- **Boss Alert Level** (0-5): Boss's awareness of worker slacking

## 2. Architecture

### 2.1 Module Structure

```
chillmcp/
├── core/                   # Core business logic
│   ├── config.py          # Constants and defaults
│   ├── state.py           # Thread-safe state management
│   ├── scheduler.py       # Background task scheduling
│   ├── events.py          # Pub/sub event system
│   ├── validators.py      # Response format validation
│   └── utils.py           # Utility functions
├── tools/                  # Break activity tools
│   ├── base.py            # Abstract base tool
│   ├── basic/             # 3 basic break tools
│   └── advanced/          # 5 advanced break tools
├── server/                 # MCP server layer
│   └── mcp_server.py      # FastMCP adapter
├── cli.py                  # CLI argument parsing
└── main.py                 # Application entry point
```

### 2.2 Design Patterns

1. **State Pattern**: `OfficeState` encapsulates state management
2. **Template Method**: `BaseTool` defines break execution template
3. **Observer Pattern**: Event bus for state change notifications
4. **Factory Pattern**: `create_mcp_server()` builds server with tools

## 3. Core Components

### 3.1 State Management (core/state.py)

**OfficeState Class**

Thread-safe state manager using `asyncio.Lock`:

```python
class OfficeState:
    - stress_level: int (0-100)
    - boss_alert_level: int (0-5)
    - boss_alertness: int (CLI parameter)
    - boss_alertness_cooldown: int (CLI parameter)
    - last_break_time: float
```

**State Transition Rules:**

| Event | Stress Change | Boss Alert Change |
|-------|---------------|-------------------|
| Take break | -Random(tool range) | +1 (probabilistic) |
| 1 min idle | +1 | 0 |
| Cooldown period | 0 | -1 |
| Boss catches (level 5) | 0 | 0 (+ 20s delay) |

### 3.2 Background Scheduler (core/scheduler.py)

**Tasks:**

1. **stress_increase_loop()**
   - Runs every 60 seconds
   - Checks time since last break
   - Increases stress by 1 if ≥60s

2. **boss_alert_decrease_loop()**
   - Runs every `boss_alertness_cooldown` seconds
   - Decreases boss_alert_level by 1

3. **check_boss_and_delay()**
   - Checks if boss_alert_level == 5
   - Applies 20-second sleep if true

### 3.3 Event System (core/events.py)

**Event Types:**
- `STRESS_INCREASED`
- `STRESS_DECREASED`
- `BOSS_ALERT_INCREASED`
- `BOSS_ALERT_DECREASED`
- `BOSS_CAUGHT` (level 5 reached)
- `BREAK_TAKEN`

**Usage:**
```python
await event_bus.publish(EventType.STRESS_DECREASED, {
    "old_value": 60,
    "new_value": 50,
    "change": -10
})
```

### 3.4 Validators (core/validators.py)

**Response Format:**
```
💬 Break Summary: <activity>
Stress Level: <int 0-100>
Boss Alert Level: <int 0-5>
```

**Validation Patterns:**
```python
BREAK_SUMMARY_PATTERN = r"Break Summary:\s*(.+?)(?:\n|$)"
STRESS_LEVEL_PATTERN = r"Stress Level:\s*(\d{1,3})"
BOSS_ALERT_PATTERN = r"Boss Alert Level:\s*([0-5])"
```

## 4. Break Tools

### 4.1 Base Tool (tools/base.py)

**BaseTool Class**

Template for all break activities:

```python
class BaseTool:
    def __init__(name, stress_reduction_range, boss_increase_chance)
    async def execute(state: OfficeState) -> str
```

**Execution Flow:**
1. Mark break taken (update timestamp)
2. Reduce stress by random amount in range
3. Possibly increase boss alert (probabilistic)
4. Check if boss caught (apply delay if needed)
5. Return formatted response

### 4.2 Tool Risk/Reward Matrix

| Tool | Stress Reduction | Boss Risk | Risk Level |
|------|------------------|-----------|------------|
| email_organizing | 5-12 | 8% | ⭐ Very Low |
| bathroom_break | 10-20 | 10% | ⭐ Very Low |
| deep_thinking | 8-20 | 15% | ⭐⭐ Low |
| take_a_break | 5-15 | 20% | ⭐⭐ Low |
| show_meme | 8-18 | 30% | ⭐⭐⭐ Medium |
| coffee_mission | 15-30 | 35% | ⭐⭐⭐ Medium |
| urgent_call | 12-25 | 45% | ⭐⭐⭐⭐ High |
| watch_netflix | 20-40 | 60% | ⭐⭐⭐⭐⭐ Very High |

### 4.3 Boss Alert Calculation

When a break is taken:

```python
if random() < boss_increase_chance:
    if random(0, 100) < boss_alertness:
        boss_alert_level += 1
```

Two-stage probability:
1. Tool's inherent risk chance
2. Boss's alertness parameter (CLI)

## 5. CLI Interface

### 5.1 Parameters

```bash
python main.py --boss_alertness N --boss_alertness_cooldown M
```

**--boss_alertness** (0-100)
- Boss's base attention level
- Higher = more likely to notice breaks
- Affects second-stage probability in boss alert increase

**--boss_alertness_cooldown** (seconds, ≥1)
- Period between automatic boss alert decreases
- Lower = boss calms down faster

### 5.2 Validation

```python
if not (0 <= boss_alertness <= 100):
    raise ValueError("boss_alertness must be between 0 and 100")

if boss_alertness_cooldown < 1:
    raise ValueError("boss_alertness_cooldown must be at least 1 second")
```

## 6. MCP Server (server/mcp_server.py)

### 6.1 Server Creation

```python
def create_mcp_server(state: OfficeState) -> FastMCP:
    mcp = FastMCP("ChillMCP - Office Break Simulator")

    # Register 8 break tools
    @mcp.tool()
    async def take_a_break() -> str:
        return await TakeABreakTool().execute(state)

    # ... (7 more tools)

    # Bonus: status check
    @mcp.tool()
    async def check_status() -> str:
        current = await state.get_state()
        return format_response("Checking current status", ...)

    return mcp
```

### 6.2 Communication Protocol

- **Protocol**: stdio (standard input/output)
- **Framework**: FastMCP 0.3.0
- **Message Format**: JSON-RPC 2.0 (handled by FastMCP)

## 7. Concurrency & Thread Safety

### 7.1 Async Architecture

All I/O operations are async:
- State updates: `async def update_stress(...)`
- Tool execution: `async def execute(...)`
- Background tasks: `asyncio.create_task(...)`

### 7.2 Lock Protection

Critical sections protected by `asyncio.Lock`:

```python
async def update_stress(self, change: int):
    async with self._lock:
        self.stress_level = clamp(self.stress_level + change, 0, 100)
```

Prevents race conditions between:
- Background stress increase
- Break-induced stress decrease
- Boss alert updates

## 8. Configuration (core/config.py)

### 8.1 Constants

```python
# Defaults
DEFAULT_STRESS_LEVEL = 50
DEFAULT_BOSS_ALERT_LEVEL = 0

# Bounds
MIN_STRESS, MAX_STRESS = 0, 100
MIN_BOSS_ALERT, MAX_BOSS_ALERT = 0, 5

# Timings
STRESS_INCREASE_INTERVAL = 60  # 1 minute
STRESS_INCREASE_AMOUNT = 1
BOSS_CAUGHT_DELAY = 20  # seconds
```

## 9. Error Handling

### 9.1 Validation Errors

- Invalid CLI arguments → ValueError + exit
- Out-of-range parameters → Clamped to bounds
- Invalid response format → Validation result with errors list

### 9.2 Runtime Errors

- Event handler exceptions → Logged, other handlers continue
- Tool execution errors → Propagated to MCP client

## 10. Testing Strategy

### 10.1 Unit Tests

- `test_response_format.py`: Regex validation
- `test_state_progress.py`: Bounds and state changes
- `test_multi_breaks.py`: Sequential tool execution

### 10.2 Integration Tests

- `test_cli_params.py`: CLI argument validation
- `test_cooldown.py`: Background task timing

### 10.3 Manual Testing

1. Start server with various parameters
2. Execute tools via MCP client
3. Verify response format
4. Check state progression over time
5. Confirm 20s delay at boss_alert_level=5

## 11. Deployment

### 11.1 Requirements

- Python 3.11+
- fastmcp==0.3.0
- asyncio (built-in)

### 11.2 MCP Client Configuration

**Claude Desktop example:**

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "/absolute/path/to/main.py",
        "--boss_alertness", "80",
        "--boss_alertness_cooldown", "60"
      ]
    }
  }
}
```

## 12. Future Enhancements

### 12.1 Potential Features

1. **Configurable tool parameters** via CLI
2. **Persistence** - save/load state
3. **Metrics dashboard** - historical stress/boss graphs
4. **Dynamic difficulty** - boss alertness adapts to player behavior
5. **Multiple workers** - team simulation
6. **Achievements system** - unlock tools based on performance

### 12.2 Performance Optimizations

1. **Event debouncing** - reduce event spam
2. **State snapshots** - periodic checkpoints
3. **Connection pooling** - multi-client support

## 13. Version History

- **v1.0.0** (2025-10-19): Initial release
  - 8 break tools
  - Automatic state progression
  - FastMCP stdio server
  - CLI parameter support
