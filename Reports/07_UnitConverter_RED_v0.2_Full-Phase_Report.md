# 07. UnitConverter RED v0.2 전 Phase 보고서

| 항목 | 내용 |
|------|------|
| 제품 | UnitConverter — 길이 단위 변환 (CLI + GUI) |
| 작성일 | 2026-06-05 |
| 상태 | Complete — Phase 1~5 RED 설계·스켈레톤 (v0.2 TC 전체) |
| 연계 | [`06_UnitConverter_GREEN-Golden_Phase_Report.md`](./06_UnitConverter_GREEN-Golden_Phase_Report.md), [`.cursorrules`](../.cursorrules) |

---

## 1. 작업 개요

| 항목 | 내용 |
|------|------|
| **목적** | Report 06 이후 v0.2 **전 Phase** RED 설계(`/red-test-plan`) 및 스켈레톤(`/red-skeleton`) 완료 |
| **입력** | Phase 0 GREEN·Golden, PRD §5.5~§5.7, Mom Test S1~S9, ARRR Skill·Command |
| **산출물** | RED 설계표(C2C), `tests/` 15건 스켈레톤, `conftest` 픽스처 확장, 본 보고서, Transcript 06, `README.md` 갱신 |
| **범위** | Phase 1(F4) ~ Phase 5(GUI G1~G5) — **구현(GREEN) 없음** |

---

## 2. ARRR 단계 (본 세션)

| 구분 | Command | 역할 | 산출물 |
|------|---------|------|--------|
| **Discovery (Ask)** | `/red-test-plan` | C2C·RED 설계표·테스트 플랜 | 문서만 (코드 없음) |
| **Delivery (Skeleton)** | `/red-skeleton` | `pytest.fail` RED 골격 | `tests/`만 diff |

선행: Report 06 — Phase 0 GREEN 3건 + D-T3-01 Golden + 회귀 5건 (**8 passed**).

---

## 3. RED 설계 (`/red-test-plan`)

### 3.1 Phase별 묶음

| Phase | PRD | Tn / AC | Logic `D-*` | Boundary `U-*` |
|-------|-----|---------|-------------|----------------|
| **0** ✅ | A1~A5 | T5, AC11 | D-T5-01, D-ARC-01, D-ARC-02 | — |
| **1** | F4, I6 | T1, AC7, AC9 | D-T1-01, D-T1-02 | U-T1-01 |
| **2** | F5, I2, O2 | T2, AC8 | D-T2-01 | U-T2-01 |
| **3~4** | F6, F7 | T4, AC4 | D-T4-01, D-T4-02 | U-T4-01 |
| **5** | G1~G5, A5 | T6, AC12 | D-T6-01, D-ARC-03 | U-GUI-01~04, U-T6-01 |

> D-T3-01(AC1 3줄)은 Report 06에서 GREEN+Golden 고정 — RED 재작성 없음.

### 3.2 Mom Test ↔ Track 매핑

| 증거 | CLI RED | GUI RED |
|------|---------|---------|
| S3·S4 오타 | D-T1-01, U-T1-01, D-T4-02 | U-GUI-02 (드롭다운) |
| S6 5분 재작업 | D-T4-01, U-T4-01 | U-GUI-04 (인라인, P1) |
| S7·S8 목표 1줄 | D-T2-01, U-T2-01 | U-GUI-03 |
| S9 정확도 | registry SSOT (I2) | U-T6-01, D-T6-01 (공유 control) |

---

## 4. RED 스켈레톤 (`/red-skeleton`)

### 4.1 `tests/conftest.py` 픽스처

| 픽스처 | 값 | Phase |
|--------|-----|-------|
| `g_meter_2_5` | `"meter:2.5"` | 공통 |
| `g_meters_typo` | `"meters:2.5"` | 1 |
| `g_meter_trimmed` | `" meter : 2.5 "` | 1 |
| `g_to_yard` | `"meter:2.5:yard"` | 2, 5 |
| `g_unknown_abc` | `"abc:1"` | 3~4, 5 |
| `g_meterss_typo` | `"meterss:1"` | 3~4 |
| `qapp` | headless `QApplication` (session) | 5 |
| `g_app_module_names` | app 모듈 목록 | 0 (GREEN) |
| `g_domain_module_names` | domain 모듈 목록 | 0 (GREEN) |

### 4.2 스켈레톤 파일 (15건)

| Phase | Test ID | 파일 |
|-------|---------|------|
| 1 | D-T1-01 | `tests/control/test_d_t1_01.py` |
| 1 | D-T1-02 | `tests/control/test_d_t1_02.py` |
| 1 | U-T1-01 | `tests/boundary/test_u_t1_01.py` |
| 2 | D-T2-01 | `tests/control/test_d_t2_01.py` |
| 2 | U-T2-01 | `tests/boundary/test_u_t2_01.py` |
| 3~4 | D-T4-01 | `tests/control/test_d_t4_01.py` |
| 3~4 | D-T4-02 | `tests/control/test_d_t4_02.py` |
| 3~4 | U-T4-01 | `tests/boundary/test_u_t4_01.py` |
| 5 | D-T6-01 | `tests/control/test_d_t6_01.py` |
| 5 | D-ARC-03 | `tests/boundary/test_d_arc_03.py` |
| 5 | U-GUI-01 | `tests/boundary/test_u_gui_01.py` |
| 5 | U-GUI-02 | `tests/boundary/test_u_gui_02.py` |
| 5 | U-GUI-03 | `tests/boundary/test_u_gui_03.py` |
| 5 | U-GUI-04 | `tests/boundary/test_u_gui_04.py` |
| 5 | U-T6-01 | `tests/boundary/test_u_t6_01.py` |

**규칙:** AAA 주석 + Then은 `pytest.fail("RED: …")` 한 줄 — assert·skip·xfail·production import 금지.

### 4.3 `tests/` 디렉터리 구조 (v0.2)

```
tests/
├── conftest.py
├── test_converter.py       # GREEN (4)
├── test_cli.py             # GREEN + Golden (1)
├── _approval.py            # Golden 헬퍼
├── ast_helpers.py          # 아키텍처 AST 가드
├── golden/
├── entity/
│   └── test_d_arc_01.py    # GREEN
├── control/
│   ├── test_d_t5_01.py     # GREEN
│   ├── test_d_arc_02.py    # GREEN
│   ├── test_d_t1_01.py     # RED
│   ├── test_d_t1_02.py     # RED
│   ├── test_d_t2_01.py     # RED
│   ├── test_d_t4_01.py     # RED
│   ├── test_d_t4_02.py     # RED
│   └── test_d_t6_01.py     # RED
└── boundary/
    ├── test_u_t1_01.py     # RED
    ├── test_u_t2_01.py     # RED
    ├── test_u_t4_01.py     # RED
    ├── test_u_gui_01.py    # RED
    ├── test_u_gui_02.py    # RED
    ├── test_u_gui_03.py    # RED
    ├── test_u_gui_04.py    # RED
    ├── test_u_t6_01.py     # RED
    └── test_d_arc_03.py    # RED
```

---

## 5. pytest 결과

가상환경(`venv/`)에서 실행:

```bash
# RED 묶음만 (15건 — 의도적 FAIL)
venv\Scripts\python.exe -m pytest tests/control/test_d_t1_01.py tests/control/test_d_t1_02.py tests/control/test_d_t2_01.py tests/control/test_d_t4_01.py tests/control/test_d_t4_02.py tests/control/test_d_t6_01.py tests/boundary/test_u_t1_01.py tests/boundary/test_u_t2_01.py tests/boundary/test_u_t4_01.py tests/boundary/test_u_gui_01.py tests/boundary/test_u_gui_02.py tests/boundary/test_u_gui_03.py tests/boundary/test_u_gui_04.py tests/boundary/test_u_t6_01.py tests/boundary/test_d_arc_03.py -v
# 15 failed

# 전체 tests/ (GREEN + RED)
venv\Scripts\python.exe -m pytest tests/ -v
# 15 failed, 8 passed
```

| 구분 | 건수 | 결과 |
|------|------|------|
| RED 스켈레톤 | 15 | **15 failed** — 의도적 `pytest.fail` |
| GREEN (Phase 0 + 회귀 + Golden) | 8 | **8 passed** |
| **합계** | 23 | 15 failed, 8 passed |

---

## 6. 전체 Test ID 현황

| Test ID | Track | Phase | 상태 | 파일 |
|---------|-------|-------|------|------|
| D-T5-01 | Logic | 0 | 🟢 GREEN | `tests/control/test_d_t5_01.py` |
| D-ARC-01 | Logic | 0 | 🟢 GREEN | `tests/entity/test_d_arc_01.py` |
| D-ARC-02 | Logic | 0 | 🟢 GREEN | `tests/control/test_d_arc_02.py` |
| D-T3-01 | UI | 3 | 🟢 GREEN + Golden | `tests/test_cli.py` |
| (회귀) domain | Logic | — | 🟢 GREEN | `tests/test_converter.py` |
| D-T1-01 | Logic | 1 | 🔴 RED | `tests/control/test_d_t1_01.py` |
| D-T1-02 | Logic | 1 | 🔴 RED | `tests/control/test_d_t1_02.py` |
| U-T1-01 | UI | 1 | 🔴 RED | `tests/boundary/test_u_t1_01.py` |
| D-T2-01 | Logic | 2 | 🔴 RED | `tests/control/test_d_t2_01.py` |
| U-T2-01 | UI | 2 | 🔴 RED | `tests/boundary/test_u_t2_01.py` |
| D-T4-01 | Logic | 3~4 | 🔴 RED | `tests/control/test_d_t4_01.py` |
| D-T4-02 | Logic | 3~4 | 🔴 RED | `tests/control/test_d_t4_02.py` |
| U-T4-01 | UI | 3~4 | 🔴 RED | `tests/boundary/test_u_t4_01.py` |
| D-T6-01 | Logic | 5 | 🔴 RED | `tests/control/test_d_t6_01.py` |
| D-ARC-03 | Logic | 5 | 🔴 RED | `tests/boundary/test_d_arc_03.py` |
| U-GUI-01 | UI | 5 | 🔴 RED | `tests/boundary/test_u_gui_01.py` |
| U-GUI-02 | UI | 5 | 🔴 RED | `tests/boundary/test_u_gui_02.py` |
| U-GUI-03 | UI | 5 | 🔴 RED | `tests/boundary/test_u_gui_03.py` |
| U-GUI-04 | UI | 5 (P1) | 🔴 RED | `tests/boundary/test_u_gui_04.py` |
| U-T6-01 | UI | 5 | 🔴 RED | `tests/boundary/test_u_t6_01.py` |

---

## 7. RED vs 구현 (프로덕션)

| 항목 | 상태 |
|------|------|
| `unit_converter/app/input_parser.py` | `parse_input`만 — `normalize_unit`·trim **미구현** |
| `unit_converter/app/output_formatter.py` | 3줄/1줄 포맷 — F5 전용 TC **미연동** |
| `unit_converter/gui_boundary.py` | **미존재** |
| `unit_converter/gui.py` (진입점) | **미존재** |
| CLI `meters:2.5` | Unknown unit (RED 전제) |

**GUI:** `PyQt6`는 `requirements.txt`에 포함. `qapp` 픽스처로 headless 테스트 준비 완료 — **실행 가능한 GUI 코드 없음**.

---

## 8. 권장 GREEN 순서

```
Phase 1 → D-T1-01 → D-T1-02 → U-T1-01 → /golden-master (선택)
Phase 2 → D-T2-01 → U-T2-01 → /golden-master (D-T2-01)
Phase 3~4 → D-T4-01 → D-T4-02 → U-T4-01
Phase 5 → U-GUI-01 → D-ARC-03 → U-GUI-02 → D-T6-01 → U-GUI-03 → U-T6-01 → U-GUI-04
```

---

## 9. 다음 단계

```
1. /green-minimal — D-T1-01 (normalize_unit 최소 구현)
2. Phase 1 GREEN 완료 후 U-T1-01, D-T1-02 순 GREEN
3. Phase 2~5 — 위 §8 순서대로 RED→GREEN
4. /golden-master — D-T2-01, U-T2-01 등 출력 계약 baseline
5. /refactor-smell — 전 Phase GREEN 후
```

---

## 10. 참고

- Phase 0 RED: [`05_UnitConverter_RED_Phase_Report.md`](./05_UnitConverter_RED_Phase_Report.md)
- Phase 0 GREEN·Golden: [`06_UnitConverter_GREEN-Golden_Phase_Report.md`](./06_UnitConverter_GREEN-Golden_Phase_Report.md)
- Transcript: [`Prompts/06_UnitConverter_RED-v0.2-Full-Phase-Transcript.md`](../Prompts/06_UnitConverter_RED-v0.2-Full-Phase-Transcript.md)
- RED ID 규칙: [`.cursor/skills/red-test-plan/reference.md`](../.cursor/skills/red-test-plan/reference.md)
- PRD: [`docs/PRD.md`](../docs/PRD.md) §5.5~§5.7, §6 (AC7~AC12)
