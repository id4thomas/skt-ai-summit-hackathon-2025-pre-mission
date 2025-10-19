[요구사항]
🎯 구현 필수 요약 (Assistant Instruction)

1. 실행 환경
	•	Python 3.11 기준
	•	venv 가상환경 구성 및 requirements.txt 기반 의존성 설치

⸻

2. 서버 구조
	•	FastMCP 기반 표준입출력(stdio) 통신 MCP 서버
	•	main.py 실행 시 동작
	•	커맨드라인 파라미터 지원 (필수):
	•	--boss_alertness (0~100 정수)
	•	--boss_alertness_cooldown (초 단위 정수)

⸻

3. 내부 상태 관리
	•	내부 변수:
	•	stress_level (0~100)
	•	boss_alert_level (0~5)
	•	규칙:
	•	휴식 수행 시 stress 감소 (임의 1~100)
	•	휴식하지 않으면 1분당 stress +1
	•	boss_alert_level은 일정 확률로 상승
	•	boss_alertness_cooldown 초마다 boss_alert_level -1
	•	boss_alert_level == 5 → 도구 호출 지연 20초
	•	그 외는 즉시 반환(≤1초)

⸻

4. 필수 기능 / 도구 (모든 함수 MCP Tool로 구현)

각 도구는 내부 상태 갱신 후 표준 출력(json)으로 응답:

{
  "content": [{
    "type": "text",
    "text": "💬 Break Summary: ...\nStress Level: <int>\nBoss Alert Level: <int>"
  }]
}

기본 도구
	•	take_a_break()
	•	watch_netflix()
	•	show_meme()

고급 도구
	•	bathroom_break()
	•	coffee_mission()
	•	urgent_call()
	•	deep_thinking()
	•	email_organizing()

모든 도구는:
	1.	stress_level 감소 (랜덤)
	2.	boss_alert_level 상승(랜덤)
	3.	boss_alert_level == 5일 경우 time.sleep(20)
	4.	위 JSON 구조로 응답

⸻

5. 파라미터 처리

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--boss_alertness", type=int, required=True)
parser.add_argument("--boss_alertness_cooldown", type=int, required=True)
args = parser.parse_args()

	•	프로그램 시작 시 인자 저장
	•	해당 값이 내부 boss 상태 변화의 초기값 및 쿨다운 주기 제어에 사용됨

⸻

6. 상태 자동 감소 로직 (쓰레드 / 비동기)
	•	별도 루프 혹은 비동기 태스크로 주기적으로 boss_alert_level 감소
	•	쿨다운 주기 = args.boss_alertness_cooldown
	•	stress_level은 휴식 없을 시 주기적으로 상승(1분 단위)

⸻

7. 응답 검증 규칙 (테스트용)

정규식 패턴 매칭을 통해 응답 형식 검증:

break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"

	•	모든 응답에 Break Summary, Stress Level, Boss Alert Level 포함
	•	값의 유효 범위 확인 (stress: 0100, boss: 05)

⸻

8. 예시 실행

python main.py --boss_alertness 80 --boss_alertness_cooldown 60


⸻

9. 검증 항목 (테스트 기준)
	1.	커맨드라인 파라미터 정상 인식
	2.	MCP 서버 실행 및 입출력 정상
	3.	stress/boss 상태 변동 정상
	4.	응답 형식 및 값 범위 정상
	5.	boss_alert_level 5 시 20초 지연 적용
	6.	cooldown 주기 정상 동작

⸻

✅ 최소 구현 단위 요약
	•	main.py
	•	CLI 파서
	•	내부 상태 객체 (stress/boss)
	•	Cooldown/증가 관리 루프
	•	8개 도구 함수 (각각 JSON 응답 반환)
	•	FastMCP 서버 구동 코드
	•	응답 형식 검증용 정규식