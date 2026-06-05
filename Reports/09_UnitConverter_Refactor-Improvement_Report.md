# 09. UnitConverter Refactor·Improvement 전 Phase 보고서

| 항목 | 내용 |
|------|------|
| 제품 | UnitConverter — 길이 단위 변환 (CLI + GUI) |
| 작성일 | 2026-06-05 |
| 상태 | Complete — Sprint A~D (Improvement Roadmap 전체) |
| 연계 | [`08_UnitConverter_GREEN-Golden_v0.2_Full-Phase_Report.md`](./08_UnitConverter_GREEN-Golden_v0.2_Full-Phase_Report.md), [`docs/Improvement_Roadmap.md`](../docs/Improvement_Roadmap.md) |

---

## 1. 작업 개요

| 항목 | 내용 |
|------|------|
| **목적** | v0.2 GREEN(23 passed) 이후 코드 스멜 분석·리팩터·로드맵 잔여(v0.3~v1.0) 일괄 완료 |
| **입력** | Report 08 종료 상태, PRD §9·§11, Mom Test S1~S9, `/refactor-smell` · `/refactor-safe` |
| **산출물** | 프로덕션·config·테스트 갱신, `docs/Code_smell.md`, `docs/Improvement_Roadmap.md`, golden 3건 갱신, 본 보고서, Transcript 08 |
| **범위** | Sprint A(v0.2 잔여) · B(v0.3 SRP/OCP) · C(v0.4 config) · D(v1.0 presenter + cubit) |

선행: Report 08 — **23 passed**.  
본 세션 종료: **31 passed**.

---

## 2. ARRR 단계 (본 세션)

| 구분 | Command / 활동 | 역할 | 산출물 |
|------|------------------|------|--------|
| **Analyze** | `/refactor-smell` | pytest PASS 전제 스멜 스캔 | `docs/Code_smell.md` |
| **Analyze** | 아키텍처 리뷰 | ECB·SSOT·AC 정합 | 채팅 보고 + 로드맵 통합 |
| **Respond** | `/refactor-safe` × N | Budget 내 구조 개선 | Sprint A~C 핵심 |
| **Respond** | 개선 루프 (GREEN 포함) | 1개 개선 → pytest | Sprint B 잔여 + CS8 + Sprint D |

---

## 3. Sprint별 완료 내역

### 3.1 Sprint A — v0.2 잔여

| ID | CS | 조치 | 파일 | pytest |
|----|-----|------|------|--------|
| A1 | CS6 | GUI `UNIT_OPTIONS` → `registry.names()` + DI | `gui_boundary.py` | 23 passed |
| A2 | CS13 | `format_value()` AC10 출력 정책 | `output_formatter.py` | 23 passed |
| A3 | G3 | GUI 인라인 오류 (기존 U-GUI-04 유지) | — | PASS |

### 3.2 Sprint C — v0.4 설정 외부화 (선행)

| ID | CS | 조치 | 파일 | pytest |
|----|-----|------|------|--------|
| C1 | CS5 | `config/units.json` + `load_config` | `config/`, `config_loader.py` | 23 passed |
| C2 | CS5 | `UnitRegistry.from_config()` | `unit_registry.py` | 23 passed |
| C3 | CS10 | aliases·`suggest_cutoff` config + `resolve_alias()` | `units.json`, `unit_registry.py`, `input_parser.py` | 24 passed |
| C4 | — | boundary composition root | `cli.py`, `gui_boundary.py` | 24 passed |

### 3.3 Sprint B — v0.3 SRP · AC11

| ID | CS | 조치 | 파일 | pytest |
|----|-----|------|------|--------|
| B1 | CS12 | `format_unknown_unit_message` → presenter | `output_formatter.py` | 24 passed |
| B2 | AC11 | T5 AST에 `conversion_flow` 포함 | `tests/conftest.py` | 24 passed |
| B3 | CS10 | `resolve_alias()` (C3 통합) | — | ✅ |
| B4 | CS10 | `UnitId` type alias | `length_unit.py` | 24 passed |
| B5 | — | `UnknownUnitError` (domain) | `domain/errors.py`, `converter.py` | 24 passed |

### 3.4 기타 · Sprint D

| ID | 조치 | 파일 | pytest |
|----|------|------|--------|
| CS1 | `_build_ui()` Extract Method | `gui_boundary.py` | 24 passed |
| CS8 | 음수 Guard Clause (GREEN) | `input_parser.py`, `test_d_t4_03.py` | 24 passed |
| CS12 | `CLI_PROMPT` 상수 | `cli.py` | 24 passed |
| D1 | json \| csv \| table Presenter Strategy | `output_formatter.py`, `input_parser.py`, `conversion_flow.py` | 30 passed |
| D2 | cubit config 등록 | `config/units.json` | 27 passed |
| D3 | `register()` · `create_builtin_unit()` | `unit_registry.py` | 31 passed |
| D4 | golden·회귀 (4단위·cubit) | `tests/golden/*.txt`, `test_cli.py` 등 | 31 passed |

---

## 4. 아키텍처·스멜 해소 요약

### 4.1 ECB · SSOT

```
config/units.json
  → infrastructure/config_loader.load_config()
  → domain/unit_registry.from_config()
  → app/conversion_flow(registry=...)
  → boundary/cli · gui_boundary (create_default_registry 주입)
```

| 원칙 | 상태 |
|------|------|
| Single Conversion Path (`convert_parsed`) | ✅ 유지 |
| boundary → app → domain | ✅ T5·D-ARC PASS |
| Registry SSOT (단위·alias·cutoff) | ✅ `units.json` |
| Presenter 단일화 | ✅ table/json/csv Strategy |

### 4.2 해소된 코드 스멜 (PRD §9)

| CS | 스멜 | 기법 |
|----|------|------|
| CS3, CS6 | 단위 목록 이중·OCP | Remove Duplication, registry SSOT |
| CS5 | Magic Number / 설정 내장 | Externalize Configuration |
| CS13 | Raw float | `format_value`, DISPLAY_PRECISION |
| CS10 | Primitive Obsession (alias) | Move Field → config/registry |
| CS12 | Hard-coded 메시지·prompt | Extract Constant, Move Method → presenter |
| CS1 | Long Method (GUI) | Extract Method `_build_ui` |
| CS8 | 음수 미검증 | Guard Clause (GREEN) |

---

## 5. 신규·갱신 파일

### 5.1 프로덕션

| 파일 | Layer | 변경 요약 |
|------|-------|-----------|
| `config/units.json` | config | meter/feet/yard/cubit, aliases, suggest_cutoff |
| `infrastructure/config_loader.py` | infra | `load_config`, `create_default_registry` |
| `domain/unit_registry.py` | domain | `from_config`, `resolve_alias`, `register`, `create_builtin_unit` |
| `domain/errors.py` | domain | **신규** — `UnknownUnitError` |
| `domain/length_unit.py` | domain | `UnitId` type alias |
| `domain/converter.py` | domain | `UnknownUnitError` 사용 |
| `app/output_formatter.py` | control | AC10, presenter, json/csv Strategy |
| `app/input_parser.py` | control | output_format 파싱, 음수 검증 |
| `app/conversion_flow.py` | control | `format_result_lines` 라우팅 |
| `cli.py` | boundary | composition root, `CLI_PROMPT` |
| `gui_boundary.py` | boundary | registry DI, `_build_ui` |

### 5.2 문서

| 파일 | 내용 |
|------|------|
| `docs/Code_smell.md` | 스멜·리팩터링 기법 매핑 |
| `docs/Improvement_Roadmap.md` | Sprint A~D 통합 로드맵 (완료) |

### 5.3 테스트

| 파일 | 내용 |
|------|------|
| `tests/control/test_d_t4_03.py` | 음수 검증 |
| `tests/control/test_d_o1_01.py` | json/csv/table presenter |
| `tests/entity/test_d_cubit_01.py` | cubit config + runtime register |
| `tests/conftest.py` | T5 `conversion_flow`, `g_negative_meter` |
| `tests/test_converter.py` | `UnknownUnitError` assert |
| `tests/golden/d_t3_01_*.txt` | cubit 4줄 반영 |
| `tests/golden/d_t4_01_*.txt`, `u_t4_01_*.txt` | cubit 지원 목록 |

---

## 6. 출력 포맷 (v1.0)

| 포맷 | 입력 예 | 출력 |
|------|---------|------|
| **table** (기본) | `meter:2.5` | 등록 단위별 O3 줄 (4줄, cubit 포함) |
| **table** | `meter:2.5:yard` | yard 1줄 |
| **csv** | `meter:2.5:csv` | header + CSV rows |
| **json** | `meter:2.5:yard:json` | `{"source":...,"conversions":[...]}` |

---

## 7. pytest (세션 종료)

```bash
venv\Scripts\python.exe -m pytest tests/ -v
# 31 passed in ~0.26s
```

| 구분 | Report 08 | Report 09 |
|------|-----------|-----------|
| 전체 | 23 | **31** |
| 신규 테스트 | — | +8 (D-T4-03, D-O1×3, D-CUBIT×4) |
| Golden 갱신 | 6 baseline | 3건 cubit 반영 (의도적) |

---

## 8. 구현 기능 요약 (사용자 관점)

| 기능 | 상태 |
|------|------|
| CLI/GUI v0.2 (F4~F7, G1~G5, AC12) | ✅ (Report 08) |
| config JSON 단위·별칭 SSOT | ✅ |
| cubit 변환 (config) | ✅ |
| 런타임 단위 `register()` | ✅ |
| JSON/CSV/table 출력 선택 | ✅ |
| AC10 일관 소수 출력 | ✅ |
| 음수 입력 거부 | ✅ |
| Improvement Roadmap | ✅ **전 항목 완료** |

---

## 9. 실행 가이드

```bash
# CLI
venv\Scripts\python.exe -m unit_converter.cli

# GUI
venv\Scripts\python.exe -m unit_converter.gui

# JSON 출력 예
# meter:2.5:yard:json

# CSV 전체 단위
# meter:2.5:csv

# 전체 테스트
venv\Scripts\python.exe -m pytest tests/ -v
```

---

## 10. 참고

- GREEN v0.2: [`08_UnitConverter_GREEN-Golden_v0.2_Full-Phase_Report.md`](./08_UnitConverter_GREEN-Golden_v0.2_Full-Phase_Report.md)
- 코드 스멜: [`docs/Code_smell.md`](../docs/Code_smell.md)
- 개선 로드맵: [`docs/Improvement_Roadmap.md`](../docs/Improvement_Roadmap.md)
- Transcript: [`Prompts/08_UnitConverter_Refactor-Improvement-Transcript.md`](../Prompts/08_UnitConverter_Refactor-Improvement-Transcript.md)
- PRD: [`docs/PRD.md`](../docs/PRD.md) §9, §11
