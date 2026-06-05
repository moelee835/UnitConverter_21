# 08. UnitConverter GREEN·Golden v0.2 전 Phase 보고서

| 항목 | 내용 |
|------|------|
| 제품 | UnitConverter — 길이 단위 변환 (CLI + GUI) |
| 작성일 | 2026-06-05 |
| 상태 | Complete — Phase 1~5 GREEN + Golden Master 6건 |
| 연계 | [`07_UnitConverter_RED_v0.2_Full-Phase_Report.md`](./07_UnitConverter_RED_v0.2_Full-Phase_Report.md), [`.cursorrules`](../.cursorrules) |

---

## 1. 작업 개요

| 항목 | 내용 |
|------|------|
| **목적** | Report 07 RED 15건을 `/green-minimal`로 GREEN하고, 출력 계약을 `/golden-master`로 baseline 고정 |
| **입력** | RED 스켈레톤 15건, Phase 0 GREEN 8건, PRD F4~F7·G1~G5, Mom Test S1~S9 |
| **산출물** | 프로덕션 5파일(신규 3·수정 2), GREEN assert 15건, golden 5건 신규, 본 보고서, Transcript 07, `README.md` 갱신 |
| **범위** | Phase 1(F4) ~ Phase 5(GUI G1~G5) — **v0.2 TC 전체 GREEN** |

선행: Report 07 — 15 failed, 8 passed.  
본 세션 종료: **23 passed**.

---

## 2. ARRR 단계 (본 세션)

| 구분 | Command | 역할 | 산출물 |
|------|---------|------|--------|
| **Respond (GREEN)** | `/green-minimal` | RED Test ID 최소 구현·assert 전환 | `app/`, `cli.py`, `gui_boundary.py`, `gui.py` |
| **Respond (Golden)** | `/golden-master` | PASS 후 출력·계약 baseline | `tests/golden/*.approved.txt` 5건 신규 |

---

## 3. GREEN Minimal (Phase 1~5)

### 3.1 Phase별 GREEN 결과

| Phase | Test ID | 구현 요약 | 결과 |
|-------|---------|-----------|------|
| **1** | D-T1-01 | `normalize_unit("meters")`→`meter` | PASSED |
| **1** | D-T1-02 | `parse_input` trim + 정규화 | PASSED |
| **1** | U-T1-01 | CLI `meters:2.5` 3줄 성공 | PASSED |
| **2** | D-T2-01 | `convert_parsed` yard 1줄 | PASSED |
| **2** | U-T2-01 | CLI `meter:2.5:yard` 1줄 | PASSED |
| **3~4** | D-T4-01 | Unknown unit 지원 목록 | PASSED |
| **3~4** | D-T4-02 | `meterss`→`Did you mean meter?` | PASSED |
| **3~4** | U-T4-01 | CLI 오류 목록·제안 | PASSED |
| **5** | D-T6-01 | 공유 `convert_parsed` 결정적 포맷 | PASSED |
| **5** | D-ARC-03 | gui_boundary → domain.converter 직접 import 0건 | PASSED |
| **5** | U-GUI-01 | `gui.py` / `gui_boundary` 진입점 | PASSED |
| **5** | U-GUI-02 | from/to 드롭다운 meter/feet/yard | PASSED |
| **5** | U-GUI-03 | GUI 목표 단위 1줄 | PASSED |
| **5** | U-GUI-04 | 인라인 오류·지원 목록 (P1) | PASSED |
| **5** | U-T6-01 | CLI·GUI 동일 결과 (AC12) | PASSED |

### 3.2 프로덕션 변경

| 파일 | Layer | 내용 |
|------|-------|------|
| `unit_converter/app/input_parser.py` | control | `normalize_unit`, `suggest_unit`, `format_unknown_unit_message`, trim |
| `unit_converter/app/conversion_flow.py` | control | **신규** — `convert_parsed()` CLI·GUI 공유 |
| `unit_converter/cli.py` | boundary | `convert_parsed` 위임 |
| `unit_converter/gui_boundary.py` | boundary | **신규** — PyQt6 `UnitConverterWindow` |
| `unit_converter/gui.py` | boundary | **신규** — `python -m unit_converter.gui` 진입점 |

**아키텍처:** `boundary → app → domain`. PyQt6는 `gui_boundary.py`만. 변환 계수 SSOT — `domain/unit_registry.py`.

### 3.3 pytest (GREEN 후)

```bash
venv\Scripts\python.exe -m pytest tests/ -v
# 23 passed
```

| 구분 | 건수 | 결과 |
|------|------|------|
| v0.2 RED→GREEN | 15 | **15 passed** |
| Phase 0 GREEN + 회귀 + Golden | 8 | **8 passed** |
| **합계** | 23 | **23 passed** |

---

## 4. Golden Master

### 4.1 baseline 목록 (6건)

| Test ID | golden 경로 | 신규/기존 |
|---------|-------------|-----------|
| D-T1-01 | `d_t1_01_meters_alias.approved.txt` | 신규 |
| D-T2-01 | `d_t2_01_g_to_yard_one_line.approved.txt` | 신규 |
| D-T3-01 | `d_t3_01_meter_2_5_three_lines.approved.txt` | 기존 (Report 06) |
| D-T4-01 | `d_t4_01_unknown_abc.approved.txt` | 신규 |
| U-T2-01 | `u_t2_01_cli_yard_only.approved.txt` | 신규 |
| U-T4-01 | `u_t4_01_unknown_with_suggestion.approved.txt` | 신규 |

### 4.2 baseline 생성·검증

```bash
# baseline 기록 (PowerShell)
$env:UPDATE_GOLDEN=1
venv\Scripts\python.exe -m pytest tests/control/test_d_t1_01.py::test_d_t1_01_meters_alias_to_meter tests/control/test_d_t2_01.py::test_d_t2_01_yard_one_line_only tests/control/test_d_t4_01.py::test_d_t4_01_unknown_lists_supported_units tests/boundary/test_u_t2_01.py::test_u_t2_01_cli_yard_only tests/boundary/test_u_t4_01.py::test_u_t4_01_unknown_with_suggestion -v

# matched 검증 (UPDATE_GOLDEN 없음)
venv\Scripts\python.exe -m pytest tests/ -v
# 23 passed — golden diff 없음
```

### 4.3 고정 계약 예시

**별칭 (D-T1-01):**

```text
input: meters
status: OK
error: NONE
lines:
line_count: 0
canonical_from: meter
```

**목표 1줄 (D-T2-01 / U-T2-01):**

```text
input: meter:2.5:yard
status: OK
error: NONE
lines:
2.5 meter = 2.734025 yard
line_count: 1
```

**Unknown (D-T4-01 / U-T4-01):**

```text
input: abc:1
status: ERROR
error: UNKNOWN_UNIT
lines:
Unknown unit: abc
Supported units: feet, meter, yard
line_count: 2
```

---

## 5. 전체 Test ID 현황

| Test ID | Track | Phase | 상태 | 파일 |
|---------|-------|-------|------|------|
| D-T5-01 | Logic | 0 | 🟢 GREEN | `tests/control/test_d_t5_01.py` |
| D-ARC-01 | Logic | 0 | 🟢 GREEN | `tests/entity/test_d_arc_01.py` |
| D-ARC-02 | Logic | 0 | 🟢 GREEN | `tests/control/test_d_arc_02.py` |
| D-T3-01 | UI | 3 | 🟢 GREEN + Golden | `tests/test_cli.py` |
| D-T1-01 | Logic | 1 | 🟢 GREEN + Golden | `tests/control/test_d_t1_01.py` |
| D-T1-02 | Logic | 1 | 🟢 GREEN | `tests/control/test_d_t1_02.py` |
| U-T1-01 | UI | 1 | 🟢 GREEN | `tests/boundary/test_u_t1_01.py` |
| D-T2-01 | Logic | 2 | 🟢 GREEN + Golden | `tests/control/test_d_t2_01.py` |
| U-T2-01 | UI | 2 | 🟢 GREEN + Golden | `tests/boundary/test_u_t2_01.py` |
| D-T4-01 | Logic | 3~4 | 🟢 GREEN + Golden | `tests/control/test_d_t4_01.py` |
| D-T4-02 | Logic | 3~4 | 🟢 GREEN | `tests/control/test_d_t4_02.py` |
| U-T4-01 | UI | 3~4 | 🟢 GREEN + Golden | `tests/boundary/test_u_t4_01.py` |
| D-T6-01 | Logic | 5 | 🟢 GREEN | `tests/control/test_d_t6_01.py` |
| D-ARC-03 | Logic | 5 | 🟢 GREEN | `tests/boundary/test_d_arc_03.py` |
| U-GUI-01~04 | UI | 5 | 🟢 GREEN | `tests/boundary/test_u_gui_*.py` |
| U-T6-01 | UI | 5 | 🟢 GREEN | `tests/boundary/test_u_t6_01.py` |
| (회귀) domain | Logic | — | 🟢 GREEN | `tests/test_converter.py` |

---

## 6. 구현 기능 요약 (사용자 관점)

### 6.1 사용 가능

| 기능 | 실행·입력 | 상태 |
|------|-----------|------|
| CLI 3줄 하위 호환 | `python -m unit_converter.cli` → `meter:2.5` | ✅ + Golden |
| 별칭·trim | `meters:2.5`, ` meter : 2.5 ` | ✅ |
| 목표 1줄 | `meter:2.5:yard` | ✅ + Golden |
| 오류 제안·목록 | `abc:1`, `meterss:1` | ✅ + Golden |
| **GUI** | `python -m unit_converter.gui` | ✅ |
| GUI from/to 드롭다운 | meter / feet / yard | ✅ |
| CLI·GUI 동일 결과 | meter 2.5 → yard | ✅ (AC12) |
| 아키텍처 가드 | T5, A4, D-ARC-03 | ✅ AST |

### 6.2 로드맵 (v0.2 이후)

| 기능 | 버전 |
|------|------|
| OCP registry 전면 | v0.3 |
| AC11 정적 검사 강화 | v0.3 |
| 설정 외부화, cubit | v0.4 |
| JSON/CSV 출력 | v1.0 |

---

## 7. 실행 가이드

```bash
# CLI
venv\Scripts\python.exe -m unit_converter.cli

# GUI (PyQt6)
venv\Scripts\python.exe -m unit_converter.gui

# 전체 테스트
venv\Scripts\python.exe -m pytest tests/ -v
```

---

## 8. 다음 단계

```
1. /refactor-smell — 전 Phase GREEN 완료(23 passed) 전제 스멜 분석
2. /refactor-safe — CS5~CS14 등 우선순위 리팩터
3. v0.3 — OCP registry, AC11 정적 검사 강화
```

---

## 9. 참고

- RED v0.2: [`07_UnitConverter_RED_v0.2_Full-Phase_Report.md`](./07_UnitConverter_RED_v0.2_Full-Phase_Report.md)
- Phase 0 GREEN·Golden: [`06_UnitConverter_GREEN-Golden_Phase_Report.md`](./06_UnitConverter_GREEN-Golden_Phase_Report.md)
- Transcript: [`Prompts/07_UnitConverter_GREEN-Golden-v0.2-Full-Phase-Transcript.md`](../Prompts/07_UnitConverter_GREEN-Golden-v0.2-Full-Phase-Transcript.md)
- Golden 포맷: [`.cursor/skills/golden-master/reference.md`](../.cursor/skills/golden-master/reference.md)
- PRD: [`docs/PRD.md`](../docs/PRD.md) §5.5~§5.7, §6 (AC7~AC12)
