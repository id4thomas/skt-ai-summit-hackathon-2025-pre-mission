# ChillMCP - 구현 문서

## 목차
1. [개요](#개요)
2. [프로젝트 구조](#프로젝트-구조)
3. [모듈별 구현 상세](#모듈별-구현-상세)
4. [실행 방법](#실행-방법)
5. [테스트](#테스트)
6. [구현 완료 체크리스트](#구현-완료-체크리스트)

---

## 개요

ChillMCP는 **모듈화된 아키텍처**로 재설계된 FastMCP 기반 MCP 서버입니다.

### 핵심 개선사항

1. **모듈화**: 기능별로 분리된 폴더 구조
2. **재사용성**: BaseTool 추상 클래스로 도구 확장 용이
3. **이벤트 시스템**: Pub/Sub 패턴으로 상태 변화 추적
4. **테스트 가능성**: 각 모듈별 독립적 테스트
5. **문서화**: 상세한 API 문서 및 사용 가이드

### 기술 스택

- **Python**: 3.11+
- **FastMCP**: 0.3.0 (MCP 서버 프레임워크)
- **asyncio**: 비동기 처리 및 동시성 제어
- **argparse**: CLI 파라미터 파싱

---

## 프로젝트 구조

```
skt-ai-summit-hackathon-2025-pre-mission/
├── main.py                         # 진입점
├── requirements.txt                # 의존성
├── IMPLEMENTATION.md               # 본 문서
├── USAGE.md                        # 사용자 가이드
├── CLAUDE.md                       # 요구사항 명세
├── README.md                       # 프로젝트 개요
├── test_validation.py              # 레거시 검증 스크립트
│
└── chillmcp/                       # 메인 패키지
    ├── __init__.py                 # 패키지 초기화
    ├── main.py                     # 실제 메인 로직
    ├── cli.py                      # CLI 파라미터 파싱
    ├── README.md                   # 패키지 문서
    │
    ├── core/                       # 핵심 로직
    │   ├── __init__.py
    │   ├── config.py               # 상수 및 기본값
    │   ├── state.py                # 상태 관리 (OfficeState)
    │   ├── scheduler.py            # 백그라운드 태스크
    │   ├── events.py               # 이벤트 Pub/Sub 시스템
    │   ├── validators.py           # 응답 형식 검증
    │   └── utils.py                # 유틸리티 함수
    │
    ├── server/                     # MCP 서버
    │   ├── __init__.py
    │   └── mcp_server.py           # FastMCP 어댑터
    │
    ├── tools/                      # 휴식 도구
    │   ├── __init__.py
    │   ├── base.py                 # BaseTool 추상 클래스
    │   ├── basic/                  # 기본 도구 (3개)
    │   │   ├── __init__.py
    │   │   ├── take_a_break.py
    │   │   ├── watch_netflix.py
    │   │   └── show_meme.py
    │   └── advanced/               # 고급 도구 (5개)
    │       ├── __init__.py
    │       ├── bathroom_break.py
    │       ├── coffee_mission.py
    │       ├── urgent_call.py
    │       ├── deep_thinking.py
    │       └── email_organizing.py
    │
    ├── tests/                      # 테스트
    │   ├── test_response_format.py
    │   ├── test_cli_params.py
    │   ├── test_state_progress.py
    │   └── test_multi_breaks.py
    │
    └── docs/                       # 문서
        ├── SPEC.md                 # 설계 명세
        └── API.md                  # API 문서
```

---

## 모듈별 구현 상세

### 1. Core 모듈 (chillmcp/core/)

#### 1.1 config.py

**위치**: `chillmcp/core/config.py`

시스템 전반에서 사용되는 상수 정의:

```python
# 기본값
DEFAULT_STRESS_LEVEL = 50
DEFAULT_BOSS_ALERT_LEVEL = 0

# 범위
MIN_STRESS, MAX_STRESS = 0, 100
MIN_BOSS_ALERT, MAX_BOSS_ALERT = 0, 5

# 타이밍
STRESS_INCREASE_INTERVAL = 60  # 초
STRESS_INCREASE_AMOUNT = 1
BOSS_CAUGHT_DELAY = 20  # 초

# CLI 파라미터 범위
MIN_BOSS_ALERTNESS = 0
MAX_BOSS_ALERTNESS = 100
MIN_COOLDOWN = 1
```

**특징**:
- 하드코딩 제거
- 중앙 집중식 설정 관리
- 타입 힌트로 명확성 향상

---

#### 1.2 utils.py

**위치**: `chillmcp/core/utils.py`

재사용 가능한 유틸리티 함수:

```python
def clamp(value, min_val, max_val):
    """값을 범위 내로 제한"""
    return max(min_val, min(max_val, value))

def rand(min_val, max_val):
    """랜덤 정수 생성"""
    return random.randint(min_val, max_val)

def now():
    """현재 타임스탬프"""
    return time.time()
```

**사용 예시**:
```python
stress = clamp(stress + change, MIN_STRESS, MAX_STRESS)
reduction = rand(5, 15)
timestamp = now()
```

---

#### 1.3 validators.py

**위치**: `chillmcp/core/validators.py`

응답 형식 검증 및 빌더:

```python
# 정규식 패턴 (요구사항 명시)
BREAK_SUMMARY_PATTERN = r"Break Summary:\s*(.+?)(?:\n|$)"
STRESS_LEVEL_PATTERN = r"Stress Level:\s*(\d{1,3})"
BOSS_ALERT_PATTERN = r"Boss Alert Level:\s*([0-5])"

def format_response(activity: str, stress: int, boss: int) -> str:
    """표준 응답 형식 생성"""
    return f"💬 Break Summary: {activity}\nStress Level: {stress}\nBoss Alert Level: {boss}"

def validate_response(response: str) -> dict:
    """응답 형식 검증 및 파싱"""
    # 정규식 매칭
    # 값 범위 검증
    # 에러 수집
    return {
        "valid": bool,
        "stress_level": int,
        "boss_alert_level": int,
        "break_summary": str,
        "errors": list
    }
```

**특징**:
- 요구사항의 정규식 패턴 정확히 구현
- 단일 책임 원칙 (응답 형식만 담당)
- 테스트 가능

---

#### 1.4 events.py

**위치**: `chillmcp/core/events.py`

Pub/Sub 이벤트 시스템:

```python
class EventType(Enum):
    STRESS_INCREASED = "stress_increased"
    STRESS_DECREASED = "stress_decreased"
    BOSS_ALERT_INCREASED = "boss_alert_increased"
    BOSS_ALERT_DECREASED = "boss_alert_decreased"
    BOSS_CAUGHT = "boss_caught"
    BREAK_TAKEN = "break_taken"

class EventBus:
    def subscribe(event_type, callback):
        """이벤트 구독"""

    async def publish(event_type, data):
        """이벤트 발행"""

# 전역 인스턴스
event_bus = EventBus()
```

**사용 예시**:
```python
# 상태 변화 시 이벤트 발행
await event_bus.publish(EventType.STRESS_DECREASED, {
    "old_value": 60,
    "new_value": 50,
    "change": -10
})

# 이벤트 구독
async def on_stress_change(data):
    print(f"Stress: {data['old_value']} → {data['new_value']}")

event_bus.subscribe(EventType.STRESS_DECREASED, on_stress_change)
```

**특징**:
- 느슨한 결합 (loose coupling)
- 확장 가능 (새 이벤트 타입 추가 용이)
- 에러 격리 (한 구독자 실패해도 다른 구독자는 계속 실행)

---

#### 1.5 state.py

**위치**: `chillmcp/core/state.py`

스레드 안전 상태 관리:

```python
class OfficeState:
    def __init__(self, boss_alertness, boss_alertness_cooldown):
        self.stress_level = DEFAULT_STRESS_LEVEL
        self.boss_alert_level = DEFAULT_BOSS_ALERT_LEVEL
        self.boss_alertness = boss_alertness
        self.boss_alertness_cooldown = boss_alertness_cooldown
        self.last_break_time = now()
        self._lock = asyncio.Lock()

    async def update_stress(self, change: int) -> int:
        """스레드 안전 스트레스 업데이트"""
        async with self._lock:
            old = self.stress_level
            self.stress_level = int(clamp(old + change, MIN_STRESS, MAX_STRESS))

            # 이벤트 발행
            if change < 0:
                await event_bus.publish(EventType.STRESS_DECREASED, {...})
            elif change > 0:
                await event_bus.publish(EventType.STRESS_INCREASED, {...})

            return self.stress_level

    async def update_boss_alert(self, change: int) -> int:
        """스레드 안전 상사 경계 업데이트"""
        async with self._lock:
            # ... (similar to update_stress)

            # Boss caught 이벤트
            if self.boss_alert_level == MAX_BOSS_ALERT:
                await event_bus.publish(EventType.BOSS_CAUGHT, {...})

    async def get_state(self) -> dict:
        """현재 상태 조회"""
        async with self._lock:
            return {
                "stress_level": self.stress_level,
                "boss_alert_level": self.boss_alert_level
            }

    async def mark_break_taken(self):
        """휴식 시간 기록"""
        async with self._lock:
            self.last_break_time = now()
            await event_bus.publish(EventType.BREAK_TAKEN, {...})
```

**특징**:
- `asyncio.Lock`으로 동시성 제어
- 모든 상태 변경은 lock 보호
- 자동 범위 검증 (clamp)
- 이벤트 발행으로 관찰 가능성 향상

---

#### 1.6 scheduler.py

**위치**: `chillmcp/core/scheduler.py`

백그라운드 태스크 관리:

```python
async def stress_increase_loop(state: OfficeState):
    """1분마다 스트레스 자동 증가"""
    while True:
        await asyncio.sleep(STRESS_INCREASE_INTERVAL)

        time_since_break = await state.get_time_since_last_break()
        if time_since_break >= STRESS_INCREASE_INTERVAL:
            await state.update_stress(STRESS_INCREASE_AMOUNT)

async def boss_alert_decrease_loop(state: OfficeState):
    """쿨다운 주기마다 상사 경계 감소"""
    while True:
        await asyncio.sleep(state.boss_alertness_cooldown)
        await state.update_boss_alert(-1)

async def check_boss_and_delay(state: OfficeState):
    """Boss 레벨 5 체크 및 지연 적용"""
    current = await state.get_state()
    if current["boss_alert_level"] == MAX_BOSS_ALERT:
        await asyncio.sleep(BOSS_CAUGHT_DELAY)

async def start_background_tasks(state: OfficeState):
    """모든 백그라운드 태스크 시작"""
    asyncio.create_task(stress_increase_loop(state))
    asyncio.create_task(boss_alert_decrease_loop(state))
```

**특징**:
- 비동기 백그라운드 실행
- 메인 로직과 분리
- 테스트 가능 (mock state 주입)

---

### 2. Tools 모듈 (chillmcp/tools/)

#### 2.1 base.py

**위치**: `chillmcp/tools/base.py`

모든 휴식 도구의 추상 기반 클래스:

```python
class BaseTool:
    """템플릿 메서드 패턴"""

    def __init__(self, name, stress_reduction_range, boss_increase_chance):
        self.name = name
        self.stress_reduction_range = stress_reduction_range
        self.boss_increase_chance = boss_increase_chance

    async def execute(self, state: OfficeState) -> str:
        """공통 실행 로직 (템플릿 메서드)"""

        # 1. 휴식 시간 기록
        await state.mark_break_taken()

        # 2. 스트레스 감소
        reduction = rand(
            self.stress_reduction_range[0],
            self.stress_reduction_range[1]
        )
        await state.update_stress(-reduction)

        # 3. 상사 경계 증가 (확률적)
        if random.random() < self.boss_increase_chance:
            if rand(0, 100) < state.boss_alertness:
                await state.update_boss_alert(1)

        # 4. Boss 감지 및 지연
        await check_boss_and_delay(state)

        # 5. 응답 생성
        final = await state.get_state()
        return format_response(
            self.name,
            final["stress_level"],
            final["boss_alert_level"]
        )
```

**설계 패턴**: Template Method Pattern

**장점**:
- 중복 코드 제거
- 일관된 동작 보장
- 새 도구 추가 용이

---

#### 2.2 기본 도구 (tools/basic/)

각 도구는 BaseTool을 상속:

**take_a_break.py**:
```python
class TakeABreakTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Taking a quick break",
            stress_reduction_range=(5, 15),
            boss_increase_chance=0.2
        )
```

**watch_netflix.py**:
```python
class WatchNetflixTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Watching Netflix",
            stress_reduction_range=(20, 40),
            boss_increase_chance=0.6
        )
```

**show_meme.py**:
```python
class ShowMemeTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Looking at memes",
            stress_reduction_range=(8, 18),
            boss_increase_chance=0.3
        )
```

---

#### 2.3 고급 도구 (tools/advanced/)

**bathroom_break.py**:
```python
class BathroomBreakTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Taking a bathroom break",
            stress_reduction_range=(10, 20),
            boss_increase_chance=0.1  # 매우 안전
        )
```

**coffee_mission.py**:
```python
class CoffeeMissionTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Going on a coffee mission",
            stress_reduction_range=(15, 30),
            boss_increase_chance=0.35
        )
```

**urgent_call.py**:
```python
class UrgentCallTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Taking an urgent personal call",
            stress_reduction_range=(12, 25),
            boss_increase_chance=0.45  # 높은 위험
        )
```

**deep_thinking.py**:
```python
class DeepThinkingTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Deep thinking (actually relaxing)",
            stress_reduction_range=(8, 20),
            boss_increase_chance=0.15
        )
```

**email_organizing.py**:
```python
class EmailOrganizingTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Organizing emails slowly",
            stress_reduction_range=(5, 12),
            boss_increase_chance=0.08  # 가장 안전
        )
```

---

#### 2.4 도구 특성 요약

| 도구 | 파일 | 스트레스 감소 | Boss 위험 | 위험도 |
|------|------|--------------|-----------|--------|
| take_a_break | basic/take_a_break.py | 5-15 | 20% | ⭐⭐ |
| watch_netflix | basic/watch_netflix.py | 20-40 | 60% | ⭐⭐⭐⭐⭐ |
| show_meme | basic/show_meme.py | 8-18 | 30% | ⭐⭐⭐ |
| bathroom_break | advanced/bathroom_break.py | 10-20 | 10% | ⭐ |
| coffee_mission | advanced/coffee_mission.py | 15-30 | 35% | ⭐⭐⭐ |
| urgent_call | advanced/urgent_call.py | 12-25 | 45% | ⭐⭐⭐⭐ |
| deep_thinking | advanced/deep_thinking.py | 8-20 | 15% | ⭐⭐ |
| email_organizing | advanced/email_organizing.py | 5-12 | 8% | ⭐ |

---

### 3. Server 모듈 (chillmcp/server/)

#### 3.1 mcp_server.py

**위치**: `chillmcp/server/mcp_server.py`

FastMCP 서버 어댑터:

```python
def create_mcp_server(state: OfficeState) -> FastMCP:
    """MCP 서버 생성 및 도구 등록"""

    mcp = FastMCP("ChillMCP - Office Break Simulator")

    # 도구 인스턴스 생성
    tools = {
        "take_a_break": TakeABreakTool(),
        "watch_netflix": WatchNetflixTool(),
        # ... (모든 도구)
    }

    # FastMCP에 등록
    @mcp.tool()
    async def take_a_break() -> str:
        """Take a quick break to reduce stress"""
        return await tools["take_a_break"].execute(state)

    # ... (나머지 7개 도구 등록)

    # 보너스: 상태 확인 도구
    @mcp.tool()
    async def check_status() -> str:
        """Check current stress and boss alert levels"""
        current = await state.get_state()
        return format_response("Checking current status", ...)

    return mcp
```

**특징**:
- Factory 패턴
- 상태 주입 (Dependency Injection)
- FastMCP 데코레이터 활용

---

### 4. CLI 모듈 (chillmcp/cli.py)

**위치**: `chillmcp/cli.py`

명령줄 인자 파싱 및 검증:

```python
def parse_args():
    """CLI 파라미터 파싱 및 검증"""

    parser = argparse.ArgumentParser(
        description="ChillMCP - Office Break Simulator MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --boss_alertness 80 --boss_alertness_cooldown 60
  %(prog)s --boss_alertness 30 --boss_alertness_cooldown 120
        """
    )

    parser.add_argument(
        "--boss_alertness",
        type=int,
        required=True,
        help=f"Boss alertness level ({MIN_BOSS_ALERTNESS}-{MAX_BOSS_ALERTNESS})"
    )

    parser.add_argument(
        "--boss_alertness_cooldown",
        type=int,
        required=True,
        help=f"Cooldown period in seconds (minimum {MIN_COOLDOWN})"
    )

    args = parser.parse_args()

    # 검증
    if not (MIN_BOSS_ALERTNESS <= args.boss_alertness <= MAX_BOSS_ALERTNESS):
        raise ValueError(f"boss_alertness must be between ...")

    if args.boss_alertness_cooldown < MIN_COOLDOWN:
        raise ValueError(f"boss_alertness_cooldown must be at least ...")

    return args
```

**특징**:
- 타입 검증 (type=int)
- 범위 검증 (ValueError)
- 사용 예시 포함
- 단일 책임 (CLI만 담당)

---

### 5. Main 모듈 (chillmcp/main.py, main.py)

#### 5.1 chillmcp/main.py

**위치**: `chillmcp/main.py`

실제 메인 로직:

```python
def main():
    """메인 진입점"""

    # 1. CLI 파라미터 파싱
    args = parse_args()

    # 2. 상태 초기화
    state = OfficeState(
        boss_alertness=args.boss_alertness,
        boss_alertness_cooldown=args.boss_alertness_cooldown
    )

    # 3. MCP 서버 생성
    mcp = create_mcp_server(state)

    # 4. 이벤트 루프 생성
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # 5. 백그라운드 태스크 시작
    loop.create_task(start_background_tasks(state))

    # 6. MCP 서버 실행 (stdio)
    mcp.run()
```

#### 5.2 main.py (최상위)

**위치**: `main.py`

진입점 forwarding:

```python
#!/usr/bin/env python3
from chillmcp.main import main

if __name__ == "__main__":
    main()
```

**목적**:
- 요구사항 준수 (main.py는 최상위에 위치)
- 실제 로직은 패키지 내부 (chillmcp/main.py)

---

## 실행 방법

### 1. 의존성 설치

```bash
# 가상환경 생성 (권장)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt
```

### 2. 서버 실행

```bash
python main.py --boss_alertness 80 --boss_alertness_cooldown 60
```

### 3. Claude Desktop 연결

**설정 파일**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

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

자세한 사용법은 [USAGE.md](USAGE.md) 참조.

---

## 테스트

### 1. 응답 형식 테스트

**파일**: `chillmcp/tests/test_response_format.py`

```bash
python3 chillmcp/tests/test_response_format.py
```

**검증 항목**:
- 정규식 패턴 매칭
- 값 범위 검증 (stress: 0-100, boss: 0-5)
- 필수 필드 존재 여부

### 2. 상태 진행 테스트

**파일**: `chillmcp/tests/test_state_progress.py`

```bash
python3 chillmcp/tests/test_state_progress.py
```

**검증 항목**:
- 스트레스/Boss 레벨 범위 제한
- 상태 변경 로직
- Lock 동시성 제어

### 3. 다중 휴식 테스트

**파일**: `chillmcp/tests/test_multi_breaks.py`

```bash
python3 chillmcp/tests/test_multi_breaks.py
```

**검증 항목**:
- 순차적 도구 실행
- 상태 누적 변화
- 도구별 동작 차이

### 4. CLI 파라미터 테스트

**파일**: `chillmcp/tests/test_cli_params.py`

```bash
python3 chillmcp/tests/test_cli_params.py
```

**검증 항목**:
- 유효 파라미터 허용
- 무효 파라미터 거부
- 에러 메시지 정확성

---

## 구현 완료 체크리스트

### 필수 요구사항

- ✅ **실행 환경**: Python 3.11 기반
- ✅ **가상환경**: venv 구성 가능
- ✅ **의존성**: requirements.txt (fastmcp==0.3.0)

### 서버 구조

- ✅ **FastMCP 기반**: stdio 통신
- ✅ **main.py 실행**: 최상위 진입점
- ✅ **CLI 파라미터**: `--boss_alertness`, `--boss_alertness_cooldown`

### 내부 상태 관리

- ✅ **stress_level**: 0~100 범위, 자동 증감
- ✅ **boss_alert_level**: 0~5 범위, 자동 증감
- ✅ **휴식 시 stress 감소**: 랜덤 값 (도구별 범위)
- ✅ **1분당 stress +1**: 휴식 없을 시
- ✅ **쿨다운마다 boss -1**: 백그라운드 태스크
- ✅ **boss_alert_level == 5**: 20초 지연
- ✅ **그 외**: 즉시 반환 (≤1초)

### MCP 도구 구현 (8개)

- ✅ **take_a_break**: 기본/빠른 휴식
- ✅ **watch_netflix**: 기본/Netflix
- ✅ **show_meme**: 기본/밈
- ✅ **bathroom_break**: 고급/화장실
- ✅ **coffee_mission**: 고급/커피
- ✅ **urgent_call**: 고급/긴급 전화
- ✅ **deep_thinking**: 고급/깊은 생각
- ✅ **email_organizing**: 고급/이메일 정리

### 응답 형식

- ✅ **표준 형식**: "Break Summary / Stress Level / Boss Alert Level"
- ✅ **정규식 검증**: 패턴 매칭
- ✅ **값 범위**: stress (0-100), boss (0-5)

### 추가 구현

- ✅ **모듈화**: 폴더 계층 구조
- ✅ **이벤트 시스템**: Pub/Sub 패턴
- ✅ **템플릿 메서드**: BaseTool 추상 클래스
- ✅ **테스트**: 4개 테스트 파일
- ✅ **문서화**: README, SPEC, API, USAGE, IMPLEMENTATION

---

## 코드 위치 참조표

### Core 모듈

| 기능 | 파일 | 주요 클래스/함수 |
|------|------|----------------|
| 설정 상수 | chillmcp/core/config.py | (상수들) |
| 상태 관리 | chillmcp/core/state.py | OfficeState |
| 스케줄러 | chillmcp/core/scheduler.py | stress_increase_loop, boss_alert_decrease_loop |
| 이벤트 | chillmcp/core/events.py | EventBus, EventType |
| 검증 | chillmcp/core/validators.py | validate_response, format_response |
| 유틸 | chillmcp/core/utils.py | clamp, rand, now |

### Tools 모듈

| 도구 | 파일 | 클래스 |
|------|------|-------|
| 기반 | chillmcp/tools/base.py | BaseTool |
| 빠른 휴식 | chillmcp/tools/basic/take_a_break.py | TakeABreakTool |
| Netflix | chillmcp/tools/basic/watch_netflix.py | WatchNetflixTool |
| 밈 | chillmcp/tools/basic/show_meme.py | ShowMemeTool |
| 화장실 | chillmcp/tools/advanced/bathroom_break.py | BathroomBreakTool |
| 커피 | chillmcp/tools/advanced/coffee_mission.py | CoffeeMissionTool |
| 전화 | chillmcp/tools/advanced/urgent_call.py | UrgentCallTool |
| 사색 | chillmcp/tools/advanced/deep_thinking.py | DeepThinkingTool |
| 이메일 | chillmcp/tools/advanced/email_organizing.py | EmailOrganizingTool |

### 서버 & CLI

| 기능 | 파일 | 주요 함수 |
|------|------|----------|
| MCP 서버 | chillmcp/server/mcp_server.py | create_mcp_server |
| CLI 파싱 | chillmcp/cli.py | parse_args |
| 메인 로직 | chillmcp/main.py | main |
| 진입점 | main.py | (forwarding) |

### 테스트

| 테스트 | 파일 | 검증 내용 |
|--------|------|----------|
| 응답 형식 | chillmcp/tests/test_response_format.py | 정규식, 값 범위 |
| CLI 파라미터 | chillmcp/tests/test_cli_params.py | 파라미터 검증 |
| 상태 진행 | chillmcp/tests/test_state_progress.py | 범위 제한, 상태 변화 |
| 다중 휴식 | chillmcp/tests/test_multi_breaks.py | 순차 실행, 누적 |

---

## 설계 패턴

### 1. Template Method Pattern

**위치**: `chillmcp/tools/base.py`

BaseTool.execute()가 템플릿 메서드로, 공통 로직을 정의하고 하위 클래스는 파라미터만 제공.

### 2. Factory Pattern

**위치**: `chillmcp/server/mcp_server.py`

create_mcp_server()가 팩토리 함수로, 설정된 MCP 서버 인스턴스 생성.

### 3. Observer Pattern (Pub/Sub)

**위치**: `chillmcp/core/events.py`

EventBus를 통한 이벤트 기반 통신. 상태 변화를 관찰자들에게 알림.

### 4. Dependency Injection

**위치**: 전역

OfficeState 인스턴스를 각 모듈에 주입하여 결합도 낮춤.

---

## 아키텍처 다이어그램

```
┌───────────────────────────────────────────────────┐
│                    main.py                        │
│              (Entry Point / CLI)                  │
└────────────────────┬──────────────────────────────┘
                     │
         ┌───────────▼────────────┐
         │   chillmcp/main.py     │
         │  (Main Logic)          │
         └───────┬───────┬────────┘
                 │       │
    ┌────────────▼──┐  ┌▼─────────────┐
    │   cli.py      │  │ server/      │
    │ (Parse Args)  │  │ mcp_server   │
    └───────────────┘  └──┬───────────┘
                          │
         ┌────────────────┴────────────────┐
         │                                  │
    ┌────▼─────┐                      ┌────▼─────┐
    │  core/   │                      │  tools/  │
    │  state   │◄─────────────────────┤  base    │
    │  events  │                      │  basic/  │
    │  scheduler│                     │  advanced/│
    │  validators│                    └──────────┘
    │  utils   │
    └──────────┘
```

---

## 버전 정보

- **버전**: 1.0.0
- **작성일**: 2025-10-19
- **Python**: 3.11+
- **FastMCP**: 0.3.0

---

## 관련 문서

- [README.md](chillmcp/README.md): 프로젝트 개요
- [USAGE.md](USAGE.md): 사용자 가이드
- [docs/SPEC.md](chillmcp/docs/SPEC.md): 설계 명세
- [docs/API.md](chillmcp/docs/API.md): API 문서
- [CLAUDE.md](CLAUDE.md): 원본 요구사항

---

## 라이선스

SKT AI Summit Hackathon 2025 Pre-mission
