# ChillMCP - Design Specification

## Overview

ChillMCP is an MCP (Model Context Protocol) server that provides AI agents with tools to manage stress and take breaks, humorously simulating "office slacking" behaviors while maintaining productivity awareness through a boss alertness system.

## Architecture

### Component Structure

```
ChillMCP
├── Core Layer
│   ├── Configuration Management
│   ├── State Management
│   ├── Event System
│   └── Utilities
├── Scheduler Layer
│   └── Background State Updates
├── Tool Layer
│   ├── Base Tool Interface
│   ├── Basic Tools
│   └── Advanced Tools
└── Server Layer
    └── MCP Server Adapter
```

## Core Components

### 1. Configuration (`core/config.py`)

**Purpose**: Centralized configuration management

**Key Parameters**:
- `boss_alertness`: 0-100% probability of boss alert increase per break
- `boss_alertness_cooldown`: Seconds between automatic boss alert decreases
- `stress_increase_interval`: Seconds between automatic stress increases
- `stress_increase_amount`: Stress points added per interval

**Validation**: All parameters are validated on initialization

### 2. State Management (`core/state.py`)

**Purpose**: Thread-safe state tracking for AI agent

**State Variables**:
- **Stress Level**: 0-100 range
  - Increases automatically over time (minimum 1 point/minute)
  - Decreases when tools are used (1-100 points randomly)
- **Boss Alert Level**: 0-5 range
  - Increases randomly when breaks are taken (based on `boss_alertness`)
  - Decreases automatically based on cooldown period
  - Level 5 triggers 20-second delay on tool execution

**Thread Safety**: Uses mutex locks for all state modifications

### 3. Scheduler (`core/scheduler.py`)

**Purpose**: Background task manager for automatic state updates

**Responsibilities**:
- Runs in separate daemon thread
- Checks for stress auto-increment every update interval
- Checks for boss alert cooldown every update interval
- Notifies subscribers of state changes
- Graceful shutdown on server stop

### 4. Event System (`core/events.py`)

**Purpose**: Pub/sub event bus for state change notifications

**Event Types**:
- `stress_updated`: Fired when stress level changes
- `boss_alert_updated`: Fired when boss alert level changes
- `tool_executed`: Fired when any tool is executed
- `delay_triggered`: Fired when 20s delay is triggered

## Tool System

### Base Tool Architecture (`tools/base.py`)

**Abstract Interface**:
- `get_name()`: Tool identifier
- `get_description()`: Tool description for MCP
- `get_emoji()`: Display emoji
- `get_message()`: Execution message
- `get_break_summary()`: Activity summary

**Common Behavior**:
1. Check if delay is needed (boss alert level >= 5)
2. Apply delay if needed (20 seconds)
3. Calculate stress reduction (1-100 random)
4. Reduce agent stress level
5. Potentially increase boss alert (based on `boss_alertness`)
6. Return formatted response

### Tool Categories

#### Basic Tools
- **take_a_break**: Generic relaxation break
- **watch_netflix**: Entertainment/streaming break
- **show_meme**: Comedy/meme browsing break

#### Advanced Tools
- **bathroom_break**: Bathroom excuse with phone browsing
- **coffee_mission**: Coffee excuse with office tour
- **urgent_call**: Phone call excuse to go outside
- **deep_thinking**: Pretend to think while zoning out
- **email_organizing**: Email excuse while online shopping

## State Machine

### Stress Level State Machine

```
[0-100 Range]
    │
    ├─→ Auto-Increase (every N seconds, +1 point minimum)
    └─→ Tool Decrease (random 1-100 points per tool use)
```

**Transitions**:
- Time-based: +1 every 60s (configurable)
- Tool-based: -1 to -100 (random)
- Bounds: Clamped to [0, 100]

### Boss Alert Level State Machine

```
[0-5 Range]
    │
    ├─→ Break Trigger (probabilistic increase based on boss_alertness)
    ├─→ Auto-Decrease (every cooldown period, -1 point)
    └─→ Level 5 Effect (20s delay on all tool executions)
```

**Transitions**:
- Break-based: Random increase (probability = `boss_alertness`)
- Time-based: -1 every `boss_alertness_cooldown` seconds
- Bounds: Clamped to [0, 5]

## Response Format

### MCP Response Structure

```json
{
  "content": [
    {
      "type": "text",
      "text": "[emoji] [message]\n\nBreak Summary: [summary]\nStress Level: [0-100]\nBoss Alert Level: [0-5]"
    }
  ]
}
```

### Parsing Requirements

All responses must be parsable using these regex patterns:
- Break Summary: `Break Summary:\s*(.+?)(?:\n|$)`
- Stress Level: `Stress Level:\s*(\d{1,3})`
- Boss Alert Level: `Boss Alert Level:\s*([0-5])`

## Command-Line Interface

### Required Parameters

```bash
--boss_alertness N           # 0-100, default: 50
--boss_alertness_cooldown N  # seconds, default: 300
--stress_increase_interval N # seconds, default: 60
```

### Parameter Validation

- `boss_alertness`: Must be 0-100
- `boss_alertness_cooldown`: Must be >= 1
- `stress_increase_interval`: Must be >= 1

Invalid parameters cause immediate exit with error message.

## Threading Model

### Main Thread
- Handles MCP protocol communication (stdio)
- Processes tool execution requests
- Returns responses to client

### Scheduler Thread (Daemon)
- Runs background state updates
- Non-blocking updates
- Graceful shutdown on main thread exit

### Thread Safety
- All state access protected by mutex locks
- No race conditions between tool execution and auto-updates
- Safe concurrent read/write operations

## Performance Characteristics

### Response Time
- Normal operation: < 1 second
- Boss alert level 5: 20 seconds (intentional delay)

### State Update Frequency
- Stress auto-increment: Every 60 seconds (default)
- Boss alert cooldown: Every 300 seconds (default)
- Scheduler check interval: Every 1 second

### Resource Usage
- Single background thread
- Minimal memory footprint
- No external dependencies except FastMCP/MCP

## Design Patterns

### Patterns Used
1. **Factory Pattern**: Tool registration and creation
2. **Observer Pattern**: Event-based state notifications
3. **Strategy Pattern**: Configurable stress reduction per tool
4. **Template Method**: Base tool execution flow
5. **Singleton**: Global event bus
6. **Decorator**: MCP tool registration decorators

## Extensibility

### Adding New Tools
1. Extend `BaseTool` abstract class
2. Implement required abstract methods
3. Register in `ChillMCPServer._register_tools()`
4. Optional: Override `get_stress_reduction()` for custom logic

### Adding New State Variables
1. Add to `AgentState` class
2. Add auto-update logic to `StateScheduler`
3. Add to response format in `validators.py`
4. Update documentation

## Validation & Testing

### Validation Points
1. CLI parameter validation on startup
2. Configuration validation on creation
3. State bounds validation on every update
4. Response format validation (parsable output)

### Test Coverage Requirements
- CLI parameter parsing and validation
- State transitions (stress/boss alert)
- Tool execution with all alert levels
- Response format parsing
- Cooldown behavior
- Delay triggering at level 5
