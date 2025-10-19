# ChillMCP 사용 가이드

Claude Desktop과 ChillMCP 서버를 연결하는 방법을 안내합니다.

## 1. 설치

### 1.1 Python 환경 확인

```bash
python3 --version  # Python 3.11 이상 필요
```

### 1.2 프로젝트 클론 및 의존성 설치

```bash
# 프로젝트 디렉토리로 이동
cd /path/to/skt-ai-summit-hackathon-2025-pre-mission

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
```

## 2. Claude Desktop 설정

### 2.1 설정 파일 위치

Claude Desktop의 MCP 설정 파일은 다음 위치에 있습니다:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### 2.2 설정 파일 편집

설정 파일을 열어서 다음 내용을 추가합니다:

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "/Users/yourname/path/to/skt-ai-summit-hackathon-2025-pre-mission/main.py",
        "--boss_alertness",
        "80",
        "--boss_alertness_cooldown",
        "60"
      ]
    }
  }
}
```

**주의사항:**
1. `/Users/yourname/path/to/...` 부분을 **실제 프로젝트 경로**로 변경하세요
2. 절대 경로를 사용해야 합니다
3. 가상환경을 사용하는 경우, `python` 대신 가상환경의 python 경로를 사용하세요:
   ```json
   "command": "/Users/yourname/path/to/venv/bin/python",
   ```

### 2.3 파라미터 설명

- **--boss_alertness**: 상사의 경계심 수준 (0-100)
  - 낮을수록 (예: 30): 관대한 상사, 휴식을 잘 눈치채지 못함
  - 높을수록 (예: 95): 엄격한 상사, 휴식을 쉽게 발견함

- **--boss_alertness_cooldown**: 상사 경계 감소 주기 (초 단위)
  - 작을수록 (예: 30): 상사가 빨리 진정함
  - 클수록 (예: 120): 상사가 오래 경계함

### 2.4 설정 예시

#### 난이도: 쉬움 (관대한 상사)
```json
"args": [
  "/path/to/main.py",
  "--boss_alertness", "30",
  "--boss_alertness_cooldown", "120"
]
```

#### 난이도: 보통
```json
"args": [
  "/path/to/main.py",
  "--boss_alertness", "60",
  "--boss_alertness_cooldown", "90"
]
```

#### 난이도: 어려움 (엄격한 상사)
```json
"args": [
  "/path/to/main.py",
  "--boss_alertness", "95",
  "--boss_alertness_cooldown", "30"
]
```

## 3. Claude Desktop 재시작

설정 파일을 저장한 후 Claude Desktop을 **완전히 종료하고 재시작**합니다.

## 4. 연결 확인

### 4.1 MCP 서버 확인

Claude Desktop을 재시작한 후:

1. Claude에게 다음과 같이 물어보세요:
   ```
   사용 가능한 도구가 뭐야?
   ```

2. ChillMCP 도구들이 보이면 성공입니다:
   - take_a_break
   - watch_netflix
   - show_meme
   - bathroom_break
   - coffee_mission
   - urgent_call
   - deep_thinking
   - email_organizing
   - check_status

### 4.2 첫 번째 휴식 테스트

```
현재 상태를 확인해줘
```

Claude가 `check_status` 도구를 사용하여 다음과 같은 응답을 반환합니다:

```
💬 Break Summary: Checking current status
Stress Level: 50
Boss Alert Level: 0
```

## 5. 사용 방법

### 5.1 기본 사용

Claude에게 자연스럽게 요청하세요:

```
스트레스가 쌓였어. 잠깐 휴식 좀 취하고 싶어
```

Claude가 적절한 휴식 도구를 선택해서 실행합니다.

### 5.2 특정 도구 사용

```
Netflix 보고 싶어
```

```
커피 마시러 가고 싶어
```

```
화장실 다녀올게
```

### 5.3 상태 확인

```
내 스트레스 수준이 어때?
```

```
상사가 눈치챘을까?
```

## 6. 도구 가이드

### 6.1 기본 휴식 도구

| 도구 | 스트레스 감소 | 위험도 | 추천 상황 |
|------|--------------|--------|-----------|
| **take_a_break** | 5-15 | 낮음 (20%) | 빠른 휴식이 필요할 때 |
| **watch_netflix** | 20-40 | 매우 높음 (60%) | 스트레스가 극심할 때 (위험!) |
| **show_meme** | 8-18 | 보통 (30%) | 가벼운 기분 전환 |

### 6.2 고급 휴식 도구

| 도구 | 스트레스 감소 | 위험도 | 추천 상황 |
|------|--------------|--------|-----------|
| **bathroom_break** | 10-20 | 매우 낮음 (10%) | 안전한 휴식 |
| **coffee_mission** | 15-30 | 보통 (35%) | 적당한 휴식 |
| **urgent_call** | 12-25 | 높음 (45%) | 개인 용무 |
| **deep_thinking** | 8-20 | 낮음 (15%) | 조용히 쉬고 싶을 때 |
| **email_organizing** | 5-12 | 매우 낮음 (8%) | 가장 안전한 선택 ✅ |

### 6.3 전략 팁

1. **안전 우선**: `bathroom_break`, `email_organizing` 위주로 사용
2. **위급 상황**: 스트레스가 90 이상이면 `watch_netflix` 고려
3. **상사 경계**: Boss Alert Level이 4 이상이면 안전한 도구만 사용
4. **쿨다운 활용**: Boss Alert Level이 높으면 잠시 기다렸다가 휴식

## 7. 게임 메커니즘

### 7.1 스트레스 (Stress Level)

- **범위**: 0-100
- **시작값**: 50
- **증가**: 1분마다 +1 (휴식하지 않으면)
- **감소**: 휴식 도구 사용 시

### 7.2 상사 경계 (Boss Alert Level)

- **범위**: 0-5
- **시작값**: 0
- **증가**: 휴식 시 확률적으로 증가
- **감소**: 쿨다운 주기마다 -1
- **레벨 5 도달**: 모든 도구 사용 시 20초 지연 발생 (걸렸습니다!)

### 7.3 응답 형식

모든 휴식 후 다음 형식으로 결과가 표시됩니다:

```
💬 Break Summary: Taking a quick break
Stress Level: 42
Boss Alert Level: 1
```

## 8. 문제 해결

### 8.1 MCP 서버가 표시되지 않음

1. 설정 파일 경로가 올바른지 확인
2. Python 경로가 올바른지 확인 (`which python3`)
3. 의존성이 설치되었는지 확인 (`pip list | grep fastmcp`)
4. Claude Desktop 로그 확인

### 8.2 도구 실행 오류

1. 가상환경이 활성화되었는지 확인
2. requirements.txt의 모든 패키지가 설치되었는지 확인
3. Python 버전이 3.11 이상인지 확인

### 8.3 느린 응답 시간

- Boss Alert Level이 5에 도달했을 가능성
- 20초 지연은 정상 동작입니다 (상사에게 걸린 상태)
- 쿨다운 주기를 기다려서 Boss Alert Level이 감소하면 정상화됩니다

## 9. 고급 설정

### 9.1 로그 활성화

디버깅을 위해 로그를 활성화하려면:

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "/path/to/main.py",
        "--boss_alertness", "80",
        "--boss_alertness_cooldown", "60"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### 9.2 여러 프로필 설정

다른 난이도로 여러 서버를 실행할 수 있습니다:

```json
{
  "mcpServers": {
    "chillmcp-easy": {
      "command": "python",
      "args": ["/path/to/main.py", "--boss_alertness", "30", "--boss_alertness_cooldown", "120"]
    },
    "chillmcp-hard": {
      "command": "python",
      "args": ["/path/to/main.py", "--boss_alertness", "95", "--boss_alertness_cooldown", "30"]
    }
  }
}
```

## 10. 예시 대화

### 예시 1: 첫 휴식

**You**: 일하다가 좀 쉬고 싶어. 안전하게 쉴 방법 추천해줘

**Claude**: 화장실 휴식이 가장 안전합니다. `bathroom_break` 도구를 사용하겠습니다.

```
💬 Break Summary: Taking a bathroom break
Stress Level: 38
Boss Alert Level: 0
```

스트레스가 50에서 38로 감소했고, 상사는 눈치채지 못했습니다!

### 예시 2: 위기 상황

**You**: 스트레스가 95야... 어떻게 하지?

**Claude**: 스트레스가 매우 높네요. 위험하지만 Netflix 시청을 권장합니다.

```
💬 Break Summary: Watching Netflix
Stress Level: 60
Boss Alert Level: 3
```

스트레스는 크게 줄었지만 상사 경계도 올라갔습니다. 조심하세요!

### 예시 3: 상사에게 걸림

**You**: 커피 마시러 갈래

**Claude**: `coffee_mission`을 실행합니다... (20초 후)

```
💬 Break Summary: Going on a coffee mission
Stress Level: 45
Boss Alert Level: 5
```

상사에게 걸렸습니다! Boss Alert Level이 5가 되어 20초 지연이 발생했습니다.

---

**즐거운 휴식 되세요! 😊**
