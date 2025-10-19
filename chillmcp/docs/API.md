# ChillMCP API Documentation

Complete API reference for ChillMCP tools and state machine.

## Table of Contents

1. [Tool APIs](#tool-apis)
2. [State Machine](#state-machine)
3. [Response Format](#response-format)
4. [Error Handling](#error-handling)

---

## Tool APIs

All tools are async functions that return formatted strings.

### Basic Tools

#### take_a_break()

Quick break with low risk.

**Signature:**
```python
async def take_a_break() -> str
```

**Parameters:** None

**Behavior:**
- Stress reduction: Random(5, 15)
- Boss increase chance: 20%
- Risk level: Low

**Example Response:**
```
💬 Break Summary: Taking a quick break
Stress Level: 42
Boss Alert Level: 1
```

**Use Case:** Quick stress relief without much risk

---

#### watch_netflix()

Watch Netflix - high stress reduction but very risky.

**Signature:**
```python
async def watch_netflix() -> str
```

**Parameters:** None

**Behavior:**
- Stress reduction: Random(20, 40)
- Boss increase chance: 60%
- Risk level: Very High

**Example Response:**
```
💬 Break Summary: Watching Netflix
Stress Level: 25
Boss Alert Level: 4
```

**Use Case:** Emergency stress relief when stress > 90

**Warning:** High chance of boss detection!

---

#### show_meme()

Look at memes for a quick laugh.

**Signature:**
```python
async def show_meme() -> str
```

**Parameters:** None

**Behavior:**
- Stress reduction: Random(8, 18)
- Boss increase chance: 30%
- Risk level: Medium

**Example Response:**
```
💬 Break Summary: Looking at memes
Stress Level: 38
Boss Alert Level: 2
```

**Use Case:** Moderate stress relief with acceptable risk

---

### Advanced Tools

#### bathroom_break()

Bathroom break - very safe option.

**Signature:**
```python
async def bathroom_break() -> str
```

**Parameters:** None

**Behavior:**
- Stress reduction: Random(10, 20)
- Boss increase chance: 10%
- Risk level: Very Low

**Example Response:**
```
💬 Break Summary: Taking a bathroom break
Stress Level: 35
Boss Alert Level: 0
```

**Use Case:** Safe stress relief option

**Recommended:** ✅ One of the safest choices

---

#### coffee_mission()

Go on a coffee mission.

**Signature:**
```python
async def coffee_mission() -> str
```

**Parameters:** None

**Behavior:**
- Stress reduction: Random(15, 30)
- Boss increase chance: 35%
- Risk level: Medium

**Example Response:**
```
💬 Break Summary: Going on a coffee mission
Stress Level: 28
Boss Alert Level: 2
```

**Use Case:** Good balance of stress relief and risk

---

#### urgent_call()

Take an 'urgent' personal call.

**Signature:**
```python
async def urgent_call() -> str
```

**Parameters:** None

**Behavior:**
- Stress reduction: Random(12, 25)
- Boss increase chance: 45%
- Risk level: High

**Example Response:**
```
💬 Break Summary: Taking an urgent personal call
Stress Level: 32
Boss Alert Level: 3
```

**Use Case:** When you really need to make a call

**Warning:** High boss detection risk

---

#### deep_thinking()

Pretend to be in deep thought while relaxing.

**Signature:**
```python
async def deep_thinking() -> str
```

**Parameters:** None

**Behavior:**
- Stress reduction: Random(8, 20)
- Boss increase chance: 15%
- Risk level: Low

**Example Response:**
```
💬 Break Summary: Deep thinking (actually relaxing)
Stress Level: 36
Boss Alert Level: 1
```

**Use Case:** Discreet stress relief

---

#### email_organizing()

Organize emails slowly while taking mental breaks.

**Signature:**
```python
async def email_organizing() -> str
```

**Parameters:** None

**Behavior:**
- Stress reduction: Random(5, 12)
- Boss increase chance: 8%
- Risk level: Very Low

**Example Response:**
```
💬 Break Summary: Organizing emails slowly
Stress Level: 43
Boss Alert Level: 0
```

**Use Case:** Safest option for stress relief

**Recommended:** ✅ Lowest boss detection risk

---

### Status Tool

#### check_status()

Check current stress and boss alert levels without taking a break.

**Signature:**
```python
async def check_status() -> str
```

**Parameters:** None

**Behavior:**
- No state changes
- Returns current stress and boss alert levels

**Example Response:**
```
💬 Break Summary: Checking current status
Stress Level: 50
Boss Alert Level: 2
```

**Use Case:** Monitor state before deciding next action

---

## State Machine

### State Variables

```python
class OfficeState:
    stress_level: int           # Range: 0-100
    boss_alert_level: int       # Range: 0-5
    boss_alertness: int         # CLI parameter (0-100)
    boss_alertness_cooldown: int  # CLI parameter (seconds)
    last_break_time: float      # Timestamp of last break
```

### State Transitions

#### Stress Level Transitions

```mermaid
[0] --take_break--> [-random(tool_range)]
[*] --1_minute_idle--> [+1]
```

**Rules:**
1. Decreases by random amount when break is taken
2. Increases by 1 every minute without break
3. Clamped to [0, 100] range

**Formula:**
```python
new_stress = clamp(stress_level + change, 0, 100)
```

#### Boss Alert Level Transitions

```mermaid
[0] --take_break--> [+1 (probabilistic)]
[*] --cooldown_period--> [-1]
[5] --> [20s delay on all actions]
```

**Rules:**
1. May increase when taking break (two-stage probability)
2. Decreases by 1 every cooldown period
3. At level 5: All actions delayed by 20 seconds
4. Clamped to [0, 5] range

**Probability Formula:**
```python
if random() < tool.boss_increase_chance:
    if random(0, 100) < state.boss_alertness:
        boss_alert_level += 1
```

### State Machine Diagram

```
┌─────────────────────────────────────────────────────┐
│                   Office State                      │
├─────────────────────────────────────────────────────┤
│  Stress: 0 ──────────────────────────────► 100      │
│           ▲                                  ▲       │
│           │ break: -random                   │       │
│           │                         idle: +1 │       │
│           └──────────────────────────────────┘       │
│                                                      │
│  Boss:   0 ──► 1 ──► 2 ──► 3 ──► 4 ──► 5           │
│           ▲                             │   │       │
│           │ cooldown: -1               │   └─► 20s delay
│           └─────────────────────────────┘           │
│              break: +1 (probabilistic)              │
└─────────────────────────────────────────────────────┘
```

### Background Processes

#### Stress Increase Loop

```python
async def stress_increase_loop(state):
    while True:
        await asyncio.sleep(60)  # Check every minute
        if time_since_last_break >= 60:
            await state.update_stress(+1)
```

**Behavior:**
- Runs every 60 seconds
- Checks if last break was > 60 seconds ago
- Increases stress by 1 if true

#### Boss Alert Decrease Loop

```python
async def boss_alert_decrease_loop(state):
    while True:
        await asyncio.sleep(state.boss_alertness_cooldown)
        await state.update_boss_alert(-1)
```

**Behavior:**
- Runs every `boss_alertness_cooldown` seconds
- Decreases boss alert level by 1
- Minimum value is 0

#### Boss Caught Check

```python
async def check_boss_and_delay(state):
    if state.boss_alert_level == 5:
        await asyncio.sleep(20)  # Caught!
```

**Behavior:**
- Called before every tool execution
- If boss_alert_level == 5, applies 20-second delay
- Simulates being caught by boss

---

## Response Format

### Standard Format

All tools return responses in this exact format:

```
💬 Break Summary: <activity_description>
Stress Level: <integer 0-100>
Boss Alert Level: <integer 0-5>
```

### Validation Regex

```python
BREAK_SUMMARY_PATTERN = r"Break Summary:\s*(.+?)(?:\n|$)"
STRESS_LEVEL_PATTERN = r"Stress Level:\s*(\d{1,3})"
BOSS_ALERT_PATTERN = r"Boss Alert Level:\s*([0-5])"
```

### Example Responses

**Valid Response:**
```
💬 Break Summary: Taking a quick break
Stress Level: 45
Boss Alert Level: 2
```

**Invalid Response (missing emoji):**
```
Break Summary: Taking a quick break
Stress Level: 45
Boss Alert Level: 2
```

**Invalid Response (out of range):**
```
💬 Break Summary: Taking a quick break
Stress Level: 150
Boss Alert Level: 2
```

### Validation Function

```python
def validate_response(response: str) -> dict:
    """
    Returns:
        {
            "valid": bool,
            "stress_level": int or None,
            "boss_alert_level": int or None,
            "break_summary": str or None,
            "errors": list[str]
        }
    """
```

---

## Error Handling

### CLI Errors

#### Invalid boss_alertness

**Input:**
```bash
python main.py --boss_alertness 150 --boss_alertness_cooldown 60
```

**Error:**
```
ValueError: boss_alertness must be between 0 and 100, got 150
```

**Exit Code:** Non-zero

---

#### Invalid cooldown

**Input:**
```bash
python main.py --boss_alertness 80 --boss_alertness_cooldown 0
```

**Error:**
```
ValueError: boss_alertness_cooldown must be at least 1 second(s), got 0
```

**Exit Code:** Non-zero

---

### Runtime Errors

#### State Bounds Violation

**Behavior:** Automatically clamped

```python
# Stress level clamping
await state.update_stress(-1000)  # stress_level becomes 0, not -950

await state.update_stress(+1000)  # stress_level becomes 100, not 1050
```

```python
# Boss alert clamping
await state.update_boss_alert(-100)  # boss_alert_level becomes 0

await state.update_boss_alert(+100)  # boss_alert_level becomes 5
```

---

#### Event Handler Errors

**Behavior:** Logged but don't stop other handlers

```python
try:
    await callback(data)
except Exception as e:
    print(f"Error in event handler: {e}")
    # Other handlers continue to execute
```

---

## MCP Protocol

### Communication

- **Protocol:** JSON-RPC 2.0 over stdio
- **Framework:** FastMCP 0.3.0
- **Transport:** Standard input/output

### Tool Registration

```python
@mcp.tool()
async def tool_name() -> str:
    """Tool description for MCP client"""
    return await tool.execute(state)
```

### Client Request Example

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "take_a_break",
    "arguments": {}
  }
}
```

### Server Response Example

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{
      "type": "text",
      "text": "💬 Break Summary: Taking a quick break\nStress Level: 42\nBoss Alert Level: 1"
    }]
  }
}
```

---

## Event System

### Event Types

```python
class EventType(Enum):
    STRESS_INCREASED = "stress_increased"
    STRESS_DECREASED = "stress_decreased"
    BOSS_ALERT_INCREASED = "boss_alert_increased"
    BOSS_ALERT_DECREASED = "boss_alert_decreased"
    BOSS_CAUGHT = "boss_caught"
    BREAK_TAKEN = "break_taken"
```

### Subscribe to Events

```python
from chillmcp.core import event_bus, EventType

async def on_stress_change(data):
    print(f"Stress changed from {data['old_value']} to {data['new_value']}")

event_bus.subscribe(EventType.STRESS_DECREASED, on_stress_change)
```

### Publish Events

```python
await event_bus.publish(EventType.STRESS_DECREASED, {
    "old_value": 60,
    "new_value": 50,
    "change": -10
})
```

---

## Performance Characteristics

### Response Times

| Scenario | Expected Time | Notes |
|----------|---------------|-------|
| Normal operation | < 1 second | boss_alert_level < 5 |
| Boss caught (level 5) | ~20 seconds | Intentional delay |
| Status check | < 100ms | No state changes |

### Concurrency

- **Thread Safety:** All state operations protected by asyncio.Lock
- **Background Tasks:** 2 concurrent tasks (stress increase, boss decrease)
- **Tool Execution:** Sequential (one at a time per state instance)

---

## Version Information

- **API Version:** 1.0.0
- **FastMCP Version:** 0.3.0
- **Python Requirement:** 3.11+
- **Protocol:** MCP (Model Context Protocol)

---

## See Also

- [SPEC.md](SPEC.md) - Design specification
- [README.md](../README.md) - Project overview
- [USAGE.md](../../USAGE.md) - User guide
- [IMPLEMENTATION.md](../../IMPLEMENTATION.md) - Implementation details
