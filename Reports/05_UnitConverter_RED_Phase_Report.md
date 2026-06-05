# 05. UnitConverter RED 단계 보고서

| 항목 | 내용 |
|------|------|
| 제품 | UnitConverter — 길이 단위 변환 (CLI + GUI) |
| 작성일 | 2026-06-05 |
| 브랜치 | `red` |
| 상태 | Complete — RED 설계·스켈레톤·문서·venv 정책 |
| 연계 | [`04_UnitConverter_Architecture_Package_Report.md`](./04_UnitConverter_Architecture_Package_Report.md), [`.cursorrules`](../.cursorrules) |

---

## 1. RED 단계 정의 (Dual Track)

| 구분 | 역할 | 산출물 | 코드 변경 |
|------|------|--------|-----------|
| **Discovery (Ask)** | `/red-test-plan` | C2C·RED 설계표·테스트 플랜 | **없음** |
| **Delivery (Skeleton)** | `/red-skeleton` | `tests/` + `conftest` + `pytest.fail` | **tests/만** |
| **Delivery (GREEN)** | `/green-minimal` | assert·최소 구현 | 다음 단계 |

본 보고서는 **Phase 0 잔여 RED 묶음**까지를 다룬다. GREEN은 `red` 브랜치 이후 `/green-minimal`에서 진행.

---

## 2. RED 묶음 (Phase 0)

### 2.1 C2C 요약

| Test ID | PRD | To-Do (판단) | Track |
|---------|-----|--------------|-------|
| **D-T5-01** | T5, AC11, A2 | app 레이어는 `print`/`input`/`tkinter`를 **참조하지 않아야** 한다 | Logic |
| **D-ARC-01** | A4 | domain은 app·cli를 **import하지 않아야** 한다 | Logic |
| **D-ARC-02** | A4 | app은 cli를 **import하지 않아야** 한다 | Logic |

### 2.2 설계표 (Logic)

| Test ID | 대상 | Given→Then | Expected RED |
|---------|------|------------|--------------|
| D-T5-01 | `app/input_parser`, `output_formatter` | AST → I/O builtins 0건 | `pytest.fail("RED: D-T5-01")` |
| D-ARC-01 | `domain/converter`, `unit_registry` | 역방향 import 0건 | `pytest.fail("RED: D-ARC-01")` |
| D-ARC-02 | `app/*` | `unit_converter.cli` import 0건 | `pytest.fail("RED: D-ARC-02")` |

### 2.3 스켈레톤 산출 (`tests/`)

| 파일 | Test ID |
|------|---------|
| `tests/conftest.py` | `g_meter_2_5`, `g_meters_typo`, `g_to_yard`, `g_app_module_names`, `g_domain_module_names` |
| `tests/control/test_d_t5_01.py` | D-T5-01 |
| `tests/entity/test_d_arc_01.py` | D-ARC-01 |
| `tests/control/test_d_arc_02.py` | D-ARC-02 |

**규칙:** AAA 주석 + Then은 `pytest.fail` 한 줄만 — assert·skip·xfail 금지.

---

## 3. pytest 결과 (RED 확인)

가상환경(`venv/`)에서 실행:

```bash
# Windows (프로젝트 루트)
venv\Scripts\python.exe -m pytest tests/control/test_d_t5_01.py tests/entity/test_d_arc_01.py tests/control/test_d_arc_02.py -v
```

| 구분 | 결과 |
|------|------|
| RED 묶음 (3건) | **3 failed** — 의도적 `pytest.fail` |
| 기존 GREEN | `test_converter.py`, `test_cli.py` — 5 passed (전체 `tests/` 실행 시) |

---

## 4. RED vs GREEN 현황

| Test ID | 상태 | 다음 |
|---------|------|------|
| D-T5-01 | 🔴 RED | AST 정적 검사 구현 (`/green-minimal`) |
| D-ARC-01 | 🔴 RED | domain import 검사 |
| D-ARC-02 | 🔴 RED | app→cli import 검사 |
| (회귀) domain 변환 | 🟢 GREEN | `tests/test_converter.py` |
| (회귀) CLI 3줄 | 🟢 GREEN | `tests/test_cli.py` |

---

## 5. 브랜치·커밋

| 항목 | 내용 |
|------|------|
| 브랜치 | `red` |
| 커밋 요약 | `feat(red): unit_converter Phase 0 package and RED skeleton` |
| 포함 | `unit_converter/`, RED tests, Report 04, Prompt 03, `.gitignore` |
| 제외 | `__pycache__/`, `venv/` (`.gitignore`) |

---

## 6. 개발 환경 — venv · requirements.txt

| 항목 | 정책 |
|------|------|
| **venv** | 없으면 `python -m venv venv`로 **생성** 후 사용 |
| **의존성** | [`requirements.txt`](../requirements.txt) SSOT — `pip install -r requirements.txt` |
| **Agent** | venv 삭제·전역 Python로 pytest **금지** |
| **실행** | `venv\Scripts\python.exe`(Win) / `venv/bin/python`(Unix) |
| **문서** | `.cursorrules` § 가상환경, `README.md` |

---

## 7. 다음 단계

```
1. /green-minimal — D-T5-01, D-ARC-01, D-ARC-02 (tests/만 assert 전환 + AST 헬퍼)
2. /red-test-plan — Phase 1: D-T1-01, U-T1-01 (F4, T1, AC7)
3. /red-skeleton → GREEN — Mom Test 별칭·trim
```

---

## 8. 참고

- 아키텍처·패키지: [`04_UnitConverter_Architecture_Package_Report.md`](./04_UnitConverter_Architecture_Package_Report.md)
- Transcript: [`Prompts/04_UnitConverter_RED-Phase-Transcript.md`](../Prompts/04_UnitConverter_RED-Phase-Transcript.md)
- RED ID 규칙: [`.cursor/skills/red-test-plan/reference.md`](../.cursor/skills/red-test-plan/reference.md)
- PRD: [`docs/PRD.md`](../docs/PRD.md) §5.5
