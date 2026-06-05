# 06. UnitConverter GREEN·Golden Master 단계 보고서

| 항목 | 내용 |
|------|------|
| 제품 | UnitConverter — 길이 단위 변환 (CLI + GUI) |
| 작성일 | 2026-06-05 |
| 상태 | Complete — Phase 0 GREEN + D-T3-01 Golden Master |
| 연계 | [`05_UnitConverter_RED_Phase_Report.md`](./05_UnitConverter_RED_Phase_Report.md), [`.cursorrules`](../.cursorrules) |

---

## 1. 작업 개요

| 항목 | 내용 |
|------|------|
| **목적** | Report 05 RED 묶음을 `/green-minimal`로 GREEN하고, PASS 출력 계약을 `/golden-master`로 baseline 고정 |
| **입력** | RED 스켈레톤 3건, 기존 GREEN (`test_converter.py`, `test_cli.py`), ARRR Skill·Command |
| **산출물** | `tests/ast_helpers.py`, GREEN assert 전환 3건, `tests/_approval.py`, `tests/golden/`, 본 보고서, Transcript 05, `README.md` 갱신 |

---

## 2. ARRR 단계 정의 (본 세션)

| 구분 | Command | 역할 | 산출물 |
|------|---------|------|--------|
| **Respond (GREEN)** | `/green-minimal` | RED Test ID 최소 구현·assert 전환 | `tests/ast_helpers.py`, assert 테스트 3건 |
| **Respond (Golden)** | `/golden-master` | PASS 후 출력·계약 baseline | `tests/_approval.py`, `tests/golden/*.approved.txt` |

선행: Report 05 RED 완료 (`pytest.fail` 3건).  
본 세션은 **프로덕션 코드 변경 없이** `tests/`만 확장 (아키텍처 가드 + golden 인프라).

---

## 3. GREEN Minimal (Phase 0 묶음)

### 3.1 C2C → GREEN 결과

| Test ID | PRD | Given→Then | 구현 |
|---------|-----|------------|------|
| **D-T5-01** | T5, AC11, A2 | app 모듈 AST → `print`/`input`/`tkinter`/`PyQt6` 0건 | `find_io_violations()` |
| **D-ARC-01** | A4 | domain → `unit_converter.app`·`cli` import 0건 | `find_import_violations()` |
| **D-ARC-02** | A4 | app → `unit_converter.cli` import 0건 | `find_import_violations()` |

### 3.2 변경 파일

| 파일 | 내용 |
|------|------|
| `tests/ast_helpers.py` | AST 파싱·I/O 금지·역방향 import 검사 헬퍼 (신규) |
| `tests/control/test_d_t5_01.py` | `pytest.fail` → assert |
| `tests/entity/test_d_arc_01.py` | `pytest.fail` → assert |
| `tests/control/test_d_arc_02.py` | `pytest.fail` → assert |

**원칙:** 상대 import(`from ..app`) 절대 경로 해석 포함. 프로덕션 `unit_converter/` 코드는 Phase 0 골격 그대로 — 검사만 추가.

### 3.3 pytest (GREEN 후)

```bash
.venv\Scripts\python.exe -m pytest tests/control/test_d_t5_01.py tests/entity/test_d_arc_01.py tests/control/test_d_arc_02.py -v
# 3 passed
```

---

## 4. Golden Master (D-T3-01)

### 4.1 대상 선정

| 후보 | 이유 |
|------|------|
| D-T5-01, D-ARC-01, D-ARC-02 | AST 검사 — 출력 계약 없음 → golden **비대상** |
| **D-T3-01** (AC1) | `meter:2.5` → CLI 3줄 — **PASS + 출력 계약** → golden **대상** |

### 4.2 산출물

| 파일 | 역할 |
|------|------|
| `tests/_approval.py` | `format_contract_output()`, `assert_matches_golden()` |
| `tests/golden/d_t3_01_meter_2_5_three_lines.approved.txt` | baseline (UTF-8, LF) |
| `tests/test_cli.py` | 기존 assert 유지 + golden assert 추가 |

### 4.3 고정 계약 (baseline)

```text
input: meter:2.5
status: OK
error: NONE
lines:
2.5 meter = 8.2021 feet
2.5 meter = 2.5 meter
2.5 meter = 2.734025 yard
line_count: 3
```

### 4.4 baseline 생성·검증

```bash
# baseline 기록
$env:UPDATE_GOLDEN=1
.venv\Scripts\python.exe -m pytest tests/test_cli.py::test_meter_2_5_prints_three_lines -v

# matched 검증 (UPDATE_GOLDEN 없음)
.venv\Scripts\python.exe -m pytest tests/test_cli.py::test_meter_2_5_prints_three_lines -v
```

| 실행 | 결과 |
|------|------|
| 단일 노드 | **passed · matched** |
| 전체 `tests/` | **8 passed** |

---

## 5. 전체 Test ID 현황

| Test ID | Track | 상태 | 파일 |
|---------|-------|------|------|
| D-T5-01 | Logic | 🟢 GREEN | `tests/control/test_d_t5_01.py` |
| D-ARC-01 | Logic | 🟢 GREEN | `tests/entity/test_d_arc_01.py` |
| D-ARC-02 | Logic | 🟢 GREEN | `tests/control/test_d_arc_02.py` |
| D-T3-01 | UI (AC1) | 🟢 GREEN + **Golden** | `tests/test_cli.py` |
| (회귀) domain 변환 | Logic | 🟢 GREEN | `tests/test_converter.py` (4 tests) |

```bash
.venv\Scripts\python.exe -m pytest tests/ -v
# 8 passed
```

---

## 6. 구현 기능 요약 (사용자 관점)

### 6.1 현재 사용 가능

| 기능 | 상태 |
|------|------|
| CLI (`python -m unit_converter.cli`) | ✅ |
| `meter:2.5` → 3단위 전체 출력 (AC1) | ✅ |
| `meter:2.5:yard` 파싱·단일 줄 변환 로직 | ✅ (CLI 경로 구현됨, golden·전용 TC는 Phase 2) |
| domain 변환 (meter/feet/yard) | ✅ |
| 레이어 분리 아키텍처 가드 (T5, A4) | ✅ AST 테스트 |

### 6.2 미구현 (Spec만)

| 기능 | Phase |
|------|-------|
| `meters` 별칭·trim (F4, AC7) | 1 |
| 목표 단위 1줄 golden (D-T2-01, F5) | 2 |
| 오류 제안·단위 목록 (F6, F7) | 4 |
| **GUI** (PyQt6, `gui_boundary`) | 5 |
| OCP registry 전면 | v0.3 |

**GUI:** `requirements.txt`에 PyQt6 포함, **실행 가능한 GUI 코드·진입점 없음**.

---

## 7. 개발 환경

| 항목 | 내용 |
|------|------|
| venv | `.venv/` (또는 `venv/`) — Agent·문서는 venv 인터프리터만 |
| 의존성 | [`requirements.txt`](../requirements.txt) — `pytest>=8.0`, `PyQt6>=6.6` |
| Golden 갱신 | `UPDATE_GOLDEN=1` pytest만 — `.approved.txt` 수동 편집 **금지** |

---

## 8. 다음 단계

```
1. /red-test-plan — Phase 1: D-T1-01, U-T1-01 (F4, T1, AC7 — meters 별칭)
2. /red-skeleton → /green-minimal → /golden-master (D-T1-01)
3. Phase 2 — D-T2-01, U-T2-01 (F5, AC8 — yard 1줄)
4. /refactor-smell — 전체 pytest PASS 전제 (현재 8 passed 충족)
```

---

## 9. 참고

- RED 단계: [`05_UnitConverter_RED_Phase_Report.md`](./05_UnitConverter_RED_Phase_Report.md)
- Transcript: [`Prompts/05_UnitConverter_GREEN-Golden-Transcript.md`](../Prompts/05_UnitConverter_GREEN-Golden-Transcript.md)
- Golden 포맷: [`.cursor/skills/golden-master/reference.md`](../.cursor/skills/golden-master/reference.md)
- PRD: [`docs/PRD.md`](../docs/PRD.md) §5.5, §6 (AC1, AC11)
