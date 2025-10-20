# ChillMCP - Usage Guide for Claude Desktop

## Installation

### 1. Prerequisites

- Python 3.11+ (required for submission/verification)
- pip (Python package manager)
- Claude Desktop app

### 2. Setup

```bash
# Clone or download the repository
cd skt-ai-summit-hackathon-2025-pre-mission

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Claude Desktop

Add ChillMCP server to your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "/absolute/path/to/skt-ai-summit-hackathon-2025-pre-mission/main.py"
      ]
    }
  }
}
```

**With custom parameters**:

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "/absolute/path/to/skt-ai-summit-hackathon-2025-pre-mission/main.py",
        "--boss_alertness", "80",
        "--boss_alertness_cooldown", "60"
      ]
    }
  }
}
```

### 4. Restart Claude Desktop

After adding the configuration, restart Claude Desktop to load the ChillMCP server.

## Available Tools

ChillMCP provides 8 break tools organized into two categories:

### Basic Tools
- `take_a_break` - General relaxation break
- `watch_netflix` - Entertainment streaming break
- `show_meme` - Comedy/meme browsing break

### Advanced Tools
- `bathroom_break` - Bathroom excuse with phone time
- `coffee_mission` - Coffee excuse with office walk
- `urgent_call` - Phone call excuse to go outside
- `deep_thinking` - Appear thoughtful while zoning out
- `email_organizing` - Email excuse for online shopping

## Prompt Examples

### Basic Usage

#### 1. Take a Quick Break
```
I need to take a break to reduce my stress. Use the take_a_break tool.
```

**Expected Response**:
```
🌴 Taking a quick break to relax...

Break Summary: Basic relaxation break
Stress Level: 45
Boss Alert Level: 1
```

#### 2. Watch Netflix
```
I want to watch some Netflix to relax. Use the watch_netflix tool.
```

**Expected Response**:
```
📺 Binging the latest K-drama...

Break Summary: Netflix break - watching series
Stress Level: 30
Boss Alert Level: 2
```

#### 3. Browse Memes
```
Show me some memes to lighten the mood. Use the show_meme tool.
```

**Expected Response**:
```
😂 Scrolling through hilarious memes...

Break Summary: Meme browsing break
Stress Level: 25
Boss Alert Level: 1
```

### Advanced Usage

#### 4. Bathroom Break Strategy
```
I need a bathroom break but want to check my phone too. Use the bathroom_break tool.
```

**Expected Response**:
```
🚽 Bathroom time! Scrolling through phone... 📱

Break Summary: Bathroom break with phone browsing
Stress Level: 40
Boss Alert Level: 3
```

#### 5. Coffee Mission
```
Let me get coffee and take a walk around the office. Use the coffee_mission tool.
```

**Expected Response**:
```
☕ Coffee time! Taking a leisurely stroll to the break room...

Break Summary: Coffee break with office tour
Stress Level: 35
Boss Alert Level: 2
```

#### 6. Urgent Call Escape
```
I need to step outside for some fresh air. Use the urgent_call tool as an excuse.
```

**Expected Response**:
```
📞 Important call coming in! Stepping outside...

Break Summary: Urgent call - outdoor break
Stress Level: 20
Boss Alert Level: 4
```

#### 7. Deep Thinking Mode
```
I want to zone out but look productive. Use the deep_thinking tool.
```

**Expected Response**:
```
🤔 Deep in thought... (actually spacing out completely)

Break Summary: Deep thinking session - strategic zoning out
Stress Level: 50
Boss Alert Level: 1
```

#### 8. Email Organizing Cover
```
Let me browse some online shops while pretending to organize emails. Use the email_organizing tool.
```

**Expected Response**:
```
📧 Organizing inbox... (browsing online shopping) 🛒

Break Summary: Email organization with online shopping
Stress Level: 38
Boss Alert Level: 2
```

### Strategic Usage

#### 9. Check Current Status
```
What's my current stress level and boss alert status?
```

*Note: You'll need to use any tool to see current state in the response*

#### 10. Stress Management Strategy
```
My stress is getting high. Use the most relaxing break tool available.
```

*Claude will choose an appropriate tool based on context*

#### 11. Boss Detection Avoidance
```
The boss alert level is high. Use a low-risk break tool that looks productive.
```

*Recommended: Use `deep_thinking` or `email_organizing` - they appear work-related*

#### 12. Multiple Break Sequence
```
I need to take several breaks today. Start with a coffee break, then check some memes, and finally take a bathroom break.
```

*Claude will execute tools in sequence and show state changes*

#### 13. Emergency Stress Relief
```
My stress level is critical! I need maximum stress relief right now.
```

*Claude may use multiple tools or the most effective ones*

#### 14. Stealthy Break Strategy
```
I want to take breaks without increasing boss suspicion. What's the best approach?
```

*Claude will recommend low-risk tools and spacing strategy*

### Monitoring and Analysis

#### 15. Monitor State Changes
```
Use the take_a_break tool and explain how it affected my stress and boss alert levels.
```

*Claude will execute and analyze the state changes*

#### 16. Boss Alert Warning Detection
```
Keep using breaks until the boss alert reaches maximum level. Show me what happens.
```

*This demonstrates the 20-second delay at alert level 5*

#### 17. Optimal Break Schedule
```
Create an optimal break schedule for the day that minimizes boss detection while managing stress.
```

*Claude will design a schedule using various tools*

### Testing Scenarios

#### 18. Rapid Break Testing
```
Use all 8 break tools in sequence and show me the final state.
```

*Tests all tools and demonstrates cumulative effects*

#### 19. Boss Alert Cooldown Test
```
Use breaks until boss alert is high, then wait and monitor how it decreases over time.
```

*Demonstrates automatic boss alert cooldown behavior*

#### 20. Stress Accumulation Test
```
Don't take any breaks for a while and tell me when my stress level increases automatically.
```

*Demonstrates automatic stress accumulation over time*

## Understanding the Response Format

Every tool response includes three key metrics:

```
[Emoji] [Activity Message]

Break Summary: [Description of break activity]
Stress Level: [0-100]
Boss Alert Level: [0-5]
```

### Stress Level (0-100)
- **0-25**: Low stress, well-rested
- **26-50**: Moderate stress, normal state
- **51-75**: High stress, break recommended
- **76-100**: Critical stress, break needed urgently

### Boss Alert Level (0-5)
- **0**: Boss completely unaware
- **1-2**: Slight suspicion (safe)
- **3-4**: Moderate suspicion (be careful)
- **5**: High alert (⚠️ 20-second delay active!)

## Advanced Features

### Boss Alert Level 5 Behavior

When boss alert reaches level 5, you'll see:

```
⚠️ Boss is watching! Waiting 20 seconds to avoid suspicion...
```

The tool execution will be delayed by 20 seconds. This is intentional and represents the need to be extra careful when the boss is actively watching.

### State Auto-Updates

**Stress Auto-Increment**:
- Increases by 1 point every 60 seconds (default)
- Represents natural work fatigue accumulation
- Continues even when not using tools

**Boss Alert Auto-Decrement**:
- Decreases by 1 point every 300 seconds / 5 minutes (default)
- Represents boss losing interest or getting distracted
- Allows recovery from high alert states

### Configuration Parameters

You can customize server behavior via command-line parameters:

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "/path/to/main.py",
        "--boss_alertness", "80",              # 80% chance of boss noticing
        "--boss_alertness_cooldown", "60",     # Boss calms down every 60s
        "--stress_increase_interval", "30"     # Stress increases every 30s
      ]
    }
  }
}
```

**Parameters**:
- `--boss_alertness`: 0-100, probability of boss noticing each break (default: 50)
- `--boss_alertness_cooldown`: Seconds between boss alert decreases (default: 300)
- `--stress_increase_interval`: Seconds between stress increases (default: 60)

### Testing Configurations

**Easy Mode** (for testing):
```bash
--boss_alertness 20 --boss_alertness_cooldown 30
```

**Hard Mode** (for challenge):
```bash
--boss_alertness 90 --boss_alertness_cooldown 600
```

**Fast Mode** (for quick testing):
```bash
--boss_alertness 50 --boss_alertness_cooldown 10 --stress_increase_interval 10
```

## Tips and Best Practices

### 1. Balance Stress and Detection
- Don't let stress get too high
- Don't take too many breaks in quick succession
- Monitor boss alert level

### 2. Strategic Tool Selection
- **Low risk**: `deep_thinking`, `email_organizing` (look productive)
- **Medium risk**: `take_a_break`, `coffee_mission`, `show_meme`
- **High risk**: `bathroom_break`, `urgent_call`, `watch_netflix`

### 3. Timing Matters
- Space out breaks to allow boss alert cooldown
- Take breaks before stress reaches critical levels
- If boss alert is high (3-4), wait before next break

### 4. Emergency Situations
- If stress is critical (>75) and boss alert is high (4-5):
  - Use low-risk tools like `deep_thinking`
  - Wait for boss alert cooldown
  - Take multiple small breaks rather than one long one

### 5. Pattern Avoidance
- Vary your break types
- Don't use the same tool repeatedly
- Randomize break timing

## Troubleshooting

### Server Not Starting
- Check Python version (3.11+ required)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check Claude Desktop logs for errors

### Tools Not Appearing
- Verify MCP server configuration in `claude_desktop_config.json`
- Ensure absolute path to `main.py` is correct
- Restart Claude Desktop after config changes

### Unexpected Delays
- Check if boss alert level is at 5
- This is expected behavior when boss is highly suspicious
- Wait for boss alert to cool down

### Parameters Not Working
- Verify parameter names: `--boss_alertness`, `--boss_alertness_cooldown`
- Check parameter values are within valid ranges
- Ensure parameters are in the `args` array in config

## Example Claude Desktop Conversation

```
User: I'm feeling stressed. What break tools do I have available?

Claude: You have access to ChillMCP with 8 break tools:
- Basic: take_a_break, watch_netflix, show_meme
- Advanced: bathroom_break, coffee_mission, urgent_call, deep_thinking, email_organizing

Let me check your current stress with a quick break.
[Uses take_a_break]

Your current stress level is 65 (high) and boss alert is at 2 (safe).
I recommend taking another break or two to get stress below 50.

User: Use the coffee mission tool.

Claude: [Uses coffee_mission]
☕ Coffee time! Taking a leisurely stroll to the break room...

Break Summary: Coffee break with office tour
Stress Level: 45
Boss Alert Level: 3

Good news! Your stress is now in a healthy range (45). Boss alert increased
to 3, so you should probably wait a bit before taking another break.
```
