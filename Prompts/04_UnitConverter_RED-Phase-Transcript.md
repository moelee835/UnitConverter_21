# 04. UnitConverter RED Phase — Prompt Export Transcript

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_21 |
| 브랜치 | `red` |
| 작성일 | 2026-06-05 |
| 세션 | RED 단계 보고서 · venv 정책 · cursorrules |

---

## Turn 1 — User

```
Reports/ 아래에 Red 단계에 대한 리포트 생성하고 Prompt Transcript 까지 만들어.

단, venv를 내가 직접 해뒀어. 이 내용을 .cursorrules에 반영하여 앞으로 개발 단계는 반드시 가상환경으로 동작하도록 수정해줘.
```

## Turn 1 — Assistant (요약)

- `Reports/05_UnitConverter_RED_Phase_Report.md` — RED 설계·스켈레톤·pytest RED/GREEN 현황·브랜치·venv 정책
- `Prompts/04_UnitConverter_RED-Phase-Transcript.md` — 본 Transcript
- `.cursorrules` — **§ 가상환경(venv)** 추가: 사용자 생성 venv 필수, Agent는 `venv` 인터프리터만 사용
- `README.md`·`docs/PRD.md` §12 — Report 05·Prompt 04·venv 실행 안내 동기화

---

## 산출물 목록

| 경로 | 설명 |
|------|------|
| `Reports/05_UnitConverter_RED_Phase_Report.md` | RED 단계 종합 보고서 |
| `Prompts/04_UnitConverter_RED-Phase-Transcript.md` | 본 Transcript |
| `.cursorrules` | venv 필수 개발 정책 |
| `README.md` | venv 전제 실행 명령 |
| `docs/PRD.md` §12 | 참고 링크 |

---

## RED Test ID (참고)

| ID | 파일 | 상태 |
|----|------|------|
| D-T5-01 | `tests/control/test_d_t5_01.py` | RED |
| D-ARC-01 | `tests/entity/test_d_arc_01.py` | RED |
| D-ARC-02 | `tests/control/test_d_arc_02.py` | RED |

---

## venv · requirements.txt 정책 (갱신)

| 역할 | 내용 |
|------|------|
| venv | 없으면 `python -m venv venv` **생성** |
| 의존성 | `requirements.txt` SSOT → `pip install -r requirements.txt` |
| Agent | `venv\Scripts\python.exe -m pytest …` (Win) / `venv/bin/python …` (Unix) |
| 금지 | 전역 `python`/`pytest`, venv 삭제, requirements 우회 설치 |

---

## Turn 2 — User

```
만약 venv 없으면 생성하라고 하고, 의존성은 requirements.txt로 관리하라고 지시해
```

## Turn 2 — Assistant (요약)

- `requirements.txt` 추가 (`pytest>=8.0`)
- `.cursorrules` — venv 없으면 Agent가 생성, 의존성 SSOT는 requirements.txt
- `README.md`, `docs/PRD.md` §12, Report 05 동기화

---

## 이전 Transcript

- [`03_UnitConverter_Architecture-RED-Transcript.md`](./03_UnitConverter_Architecture-RED-Transcript.md) — 패키지·RED 설계·스켈레톤·커밋
