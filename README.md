# ChillMCP - Office Break Simulator

SKT AI Summit Hackathon 2025 Pre-Mission

FastMCP 기반 MCP 서버로, 사무실 업무 중 스트레스와 상사의 감시 수준을 관리하는 시뮬레이터입니다.

## 프로젝트 구조

```
skt-ai-summit-hackathon-2025-pre-mission/
├── main.py                    # 진입점
├── requirements.txt           # 의존성
├── chillmcp/                  # 메인 패키지
│   ├── core/                  # 핵심 로직
│   ├── tools/                 # 휴식 도구 (8개)
│   ├── server/                # MCP 서버
│   └── tests/                 # 테스트
└── docs/                      # 문서
```

## 빠른 시작

### 설치

```bash
# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 실행

```bash
python main.py --boss_alertness 80 --boss_alertness_cooldown 60
```

## 주요 기능

- **스트레스 관리**: 0-100 범위의 스트레스 레벨 추적
- **상사 경계 시스템**: 0-5 단계의 상사 감시 레벨
- **8가지 휴식 도구**: 위험도와 효과가 다른 다양한 휴식 방법
- **자동 상태 변화**: 시간에 따른 자동 스트레스 증가 및 경계 감소
- **결과 시스템**: 상사에게 걸리면 (레벨 5) 20초 지연 발생

## 문서

| 문서 | 설명 | 링크 |
|------|------|------|
| **사용 가이드** | Claude Desktop 연결 및 사용법 | [USAGE.md](USAGE.md) |
| **구현 문서** | 전체 구현 내용 상세 설명 | [IMPLEMENTATION.md](IMPLEMENTATION.md) |
| **설계 명세** | 아키텍처 및 설계 문서 | [chillmcp/docs/SPEC.md](chillmcp/docs/SPEC.md) |
| **API 문서** | 도구 API 및 상태 머신 상세 | [chillmcp/docs/API.md](chillmcp/docs/API.md) |
| **패키지 README** | ChillMCP 패키지 개요 | [chillmcp/README.md](chillmcp/README.md) |
| **요구사항** | 원본 요구사항 명세 | [CLAUDE.md](CLAUDE.md) |

## 휴식 도구 (8개)

### 기본 도구
- **take_a_break**: 빠른 휴식 (스트레스 ↓5-15, 위험 20%)
- **watch_netflix**: Netflix 시청 (스트레스 ↓20-40, 위험 60% ⚠️)
- **show_meme**: 밈 보기 (스트레스 ↓8-18, 위험 30%)

### 고급 도구
- **bathroom_break**: 화장실 휴식 (스트레스 ↓10-20, 위험 10% ✅)
- **coffee_mission**: 커피 미션 (스트레스 ↓15-30, 위험 35%)
- **urgent_call**: 긴급 전화 (스트레스 ↓12-25, 위험 45% ⚠️)
- **deep_thinking**: 깊은 사색 (스트레스 ↓8-20, 위험 15%)
- **email_organizing**: 이메일 정리 (스트레스 ↓5-12, 위험 8% ✅ 가장 안전)

## Claude Desktop 연결

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

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

자세한 내용은 [USAGE.md](USAGE.md)를 참조하세요.

## 테스트

```bash
# 응답 형식 검증
python3 chillmcp/tests/test_response_format.py

# 상태 진행 테스트
python3 chillmcp/tests/test_state_progress.py

# 다중 휴식 테스트
python3 chillmcp/tests/test_multi_breaks.py

# CLI 파라미터 테스트
python3 chillmcp/tests/test_cli_params.py
```

## 기술 스택

- **Python**: 3.11+
- **FastMCP**: 0.3.0
- **asyncio**: 비동기 처리 및 동시성 제어

## 설계 패턴

- **Template Method Pattern**: BaseTool 클래스
- **Factory Pattern**: create_mcp_server()
- **Observer Pattern (Pub/Sub)**: EventBus
- **Dependency Injection**: 상태 주입

## 라이선스

SKT AI Summit Hackathon 2025 Pre-mission

---

**Built with [FastMCP](https://github.com/jlowin/fastmcp)**
