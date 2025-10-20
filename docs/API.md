# ChillMCP - API Reference

## Tool Catalog

All tools follow the same execution pattern and response format, but differ in their behavior and messaging.

## Response Format

All tools return responses in the following MCP-compatible format:

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

## Basic Tools

### `take_a_break`

**Description**: Take a basic break to reduce stress and relax

**Parameters**: None

**Example Response**:
```
🌴 Taking a quick break to relax...

Break Summary: Basic relaxation break
Stress Level: 45
Boss Alert Level: 1
```

**Stress Reduction**: Random 1-100 points

---

### `watch_netflix`

**Description**: Watch Netflix to reduce stress and enjoy entertainment

**Parameters**: None

**Example Response**:
```
📺 Binging the latest K-drama...

Break Summary: Netflix break - watching series
Stress Level: 30
Boss Alert Level: 2
```

**Stress Reduction**: Random 1-100 points

---

### `show_meme`

**Description**: Look at funny memes to boost mood and reduce stress

**Parameters**: None

**Example Response**:
```
😂 Scrolling through hilarious memes...

Break Summary: Meme browsing break
Stress Level: 25
Boss Alert Level: 1
```

**Stress Reduction**: Random 1-100 points

---

## Advanced Tools

### `bathroom_break`

**Description**: Pretend to go to bathroom and browse phone for stress relief

**Parameters**: None

**Example Response**:
```
🚽 Bathroom time! Scrolling through phone... 📱

Break Summary: Bathroom break with phone browsing
Stress Level: 40
Boss Alert Level: 3
```

**Stress Reduction**: Random 1-100 points

**Special Behavior**: Highly effective at stress reduction while maintaining plausible deniability

---

### `coffee_mission`

**Description**: Go get coffee as an excuse to walk around and relax

**Parameters**: None

**Example Response**:
```
☕ Coffee time! Taking a leisurely stroll to the break room...

Break Summary: Coffee break with office tour
Stress Level: 35
Boss Alert Level: 2
```

**Stress Reduction**: Random 1-100 points

**Special Behavior**: Doubles as light exercise break

---

### `urgent_call`

**Description**: Pretend to receive urgent call and step outside for fresh air

**Parameters**: None

**Example Response**:
```
📞 Important call coming in! Stepping outside...

Break Summary: Urgent call - outdoor break
Stress Level: 20
Boss Alert Level: 4
```

**Stress Reduction**: Random 1-100 points

**Special Behavior**: Provides outdoor air and escape from office environment

---

### `deep_thinking`

**Description**: Pretend to be deep in thought while actually zoning out

**Parameters**: None

**Example Response**:
```
🤔 Deep in thought... (actually spacing out completely)

Break Summary: Deep thinking session - strategic zoning out
Stress Level: 50
Boss Alert Level: 1
```

**Stress Reduction**: Random 1-100 points

**Special Behavior**: Lowest boss suspicion risk - appears productive

---

### `email_organizing`

**Description**: Pretend to organize emails while browsing online shopping sites

**Parameters**: None

**Example Response**:
```
📧 Organizing inbox... (browsing online shopping) 🛒

Break Summary: Email organization with online shopping
Stress Level: 38
Boss Alert Level: 2
```

**Stress Reduction**: Random 1-100 points

**Special Behavior**: Screen activity looks legitimate to observers

---

## State Information

### Stress Level (0-100)

**Auto-Increment Behavior**:
- Increases by 1 point every 60 seconds (default)
- Configurable via `--stress_increase_interval`
- Represents accumulated work fatigue

**Reduction Behavior**:
- Decreases by random 1-100 points per tool use
- Never goes below 0
- Represents stress relief from breaks

**Interpretation**:
- 0-25: Low stress (well rested)
- 26-50: Moderate stress (normal working state)
- 51-75: High stress (needs break soon)
- 76-100: Critical stress (urgent break needed)

### Boss Alert Level (0-5)

**Increase Behavior**:
- Increases probabilistically when tools are used
- Probability controlled by `--boss_alertness` parameter (0-100%)
- Each tool use rolls independently

**Auto-Decrease Behavior**:
- Decreases by 1 point every cooldown period
- Cooldown period controlled by `--boss_alertness_cooldown` (seconds)
- Represents boss losing interest/getting distracted

**Special Effects**:
- **Level 5**: Triggers 20-second delay on all tool executions
  - Delay message: `⚠️ Boss is watching! Waiting 20 seconds to avoid suspicion...`
  - Delay is intentional and blocks execution

**Interpretation**:
- 0: Boss completely unaware
- 1-2: Slight suspicion (safe to continue)
- 3-4: Moderate suspicion (be careful)
- 5: High alert (dangerous - 20s delay active)

## Common Patterns

### Standard Tool Execution Flow

1. **Check Boss Alert Level**
   - If level >= 5, apply 20-second delay
   - Print warning message to stderr

2. **Calculate Stress Reduction**
   - Generate random value 1-100
   - Apply to current stress level

3. **Check Boss Alertness**
   - Roll probability check against `boss_alertness` parameter
   - If successful, increase boss alert level by 1

4. **Return Response**
   - Format with current stress and boss alert levels
   - Include tool-specific message and summary

### Response Parsing

Use these regex patterns to extract values:

```python
import re

# Extract Break Summary
break_summary = re.search(r"Break Summary:\s*(.+?)(?:\n|$)", text, re.MULTILINE)

# Extract Stress Level (0-100)
stress_level = re.search(r"Stress Level:\s*(\d{1,3})", text)

# Extract Boss Alert Level (0-5)
boss_alert = re.search(r"Boss Alert Level:\s*([0-5])", text)
```

### Example Parsing Code

```python
def parse_tool_response(response_text: str) -> dict:
    """Parse tool response into structured data."""
    break_match = re.search(r"Break Summary:\s*(.+?)(?:\n|$)", response_text, re.MULTILINE)
    stress_match = re.search(r"Stress Level:\s*(\d{1,3})", response_text)
    boss_match = re.search(r"Boss Alert Level:\s*([0-5])", response_text)

    return {
        "break_summary": break_match.group(1).strip() if break_match else None,
        "stress_level": int(stress_match.group(1)) if stress_match else None,
        "boss_alert_level": int(boss_match.group(1)) if boss_match else None
    }
```

## Error Handling

### Tool Execution Errors

Tools are designed to be resilient and should not raise exceptions under normal conditions. All state operations are bounds-checked.

### Invalid State Recovery

If state becomes invalid:
- Stress level clamped to [0, 100]
- Boss alert level clamped to [0, 5]
- Timestamps reset to current time

### Thread Safety

All state modifications are protected by mutex locks. Multiple concurrent tool calls are safe.

## Performance Notes

### Response Times

- **Normal operation**: < 1 second per tool call
- **Boss alert level 5**: ~20 seconds (intentional delay)
- **State updates**: Non-blocking background operations

### Recommended Usage Patterns

1. **Check stress level** periodically
2. **Use tools proactively** before stress reaches critical levels
3. **Monitor boss alert** to avoid detection
4. **Wait for cooldown** if boss alert reaches level 5
5. **Vary tool usage** to avoid patterns

### Optimal Strategy

For minimal boss detection with maximum stress relief:
1. Prefer low-suspicion tools (`deep_thinking`, `email_organizing`)
2. Use high-risk tools (`bathroom_break`, `urgent_call`) sparingly
3. Space out breaks to allow boss alert cooldown
4. Monitor both stress and boss alert levels
