# Unit Converter (Python)

작성자:이원준, 리뷰어:손효진, 이동규, 이정수, 이현지, 이현진

![unit-converter](./unit-converter.jpg)

## Overview

길이 단위(meter, feet, yard) 간 변환 프로그램. **CLI**와 **데스크톱 GUI**를 지원하며, 새 단위 추가 시 기존 코드 변경을 최소화하도록 설계한다. 변환 로직은 테스트 코드로 검증한다.

| 버전 | 상태 | 설명 |
|------|------|------|
| v0.1 | ✅ 하위 호환 | `UnitConverter.py` 진입점 유지 |
| **v0.2** | 🔴 **Phase 1~5 RED** | 패키지 분리·Phase 0 GREEN·AC1 golden + **15건 RED 스켈레톤** — GREEN 진행 대기 |
| v0.3~ | 로드맵 | OCP registry, 설정 외부화 등 — [`docs/PRD.md`](docs/PRD.md) §11 |

**상세 요구사항:** [`docs/PRD.md`](docs/PRD.md) · Mom Test: [`docs/UnitConverter_MomTest_Report.md`](docs/UnitConverter_MomTest_Report.md)

---

## 가상환경 · 의존성

의존성은 [`requirements.txt`](requirements.txt)로 관리합니다. 실행·테스트는 **venv 인터프리터만** 사용 ([`.cursorrules`](.cursorrules) § 가상환경).

```bash
# 1) venv 없으면 생성 (프로젝트 루트)
python -m venv venv
# 또는: python -m venv .venv

# 2) 활성화 (Windows)
venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 3) 의존성 설치 (SSOT: requirements.txt)
pip install -r requirements.txt

# CLI (권장)
python -m unit_converter.cli

# Windows: 활성화 없이 직접 호출
.venv\Scripts\python.exe -m unit_converter.cli
.venv\Scripts\python.exe -m pytest tests/ -v

# 하위 호환
python UnitConverter.py

# Phase 0 아키텍처 가드 (GREEN — 3 passed)
python -m pytest tests/control/test_d_t5_01.py tests/entity/test_d_arc_01.py tests/control/test_d_arc_02.py -v

# v0.2 RED 스켈레톤 (15건 — 의도적 FAIL)
python -m pytest tests/control/test_d_t1_01.py tests/control/test_d_t1_02.py tests/control/test_d_t2_01.py tests/control/test_d_t4_01.py tests/control/test_d_t4_02.py tests/control/test_d_t6_01.py tests/boundary/ -v

# 전체 (GREEN 8 + RED 15)
python -m pytest tests/ -v

# Golden Master baseline 갱신 (수동 .approved.txt 편집 금지)
# Windows PowerShell:
$env:UPDATE_GOLDEN=1; python -m pytest tests/test_cli.py::test_meter_2_5_prints_three_lines -v

deactivate
```

새 패키지가 필요하면 `requirements.txt`에 추가한 뒤 `pip install -r requirements.txt`를 다시 실행합니다.

---

## 프로젝트 구조 (v0.2)

```
unit_converter/
├── domain/              # entity — registry, converter, length_unit (Protocol)
├── app/                 # control — input_parser, output_formatter (presenter)
├── infrastructure/      # v0.4 config_loader (스텁)
└── cli.py               # boundary — input/print

tests/
├── test_converter.py    # Domain / Logic (GREEN — 4 tests)
├── test_cli.py          # Boundary / UI (GREEN + D-T3-01 Golden)
├── _approval.py         # Golden Master 헬퍼
├── ast_helpers.py       # 아키텍처 AST 가드
├── golden/              # *.approved.txt baseline
├── conftest.py          # 공통 픽스처 (g_meters_typo, qapp 등)
├── entity/              # D-ARC-01 (GREEN)
├── control/             # D-T5-01, D-ARC-02 (GREEN) + D-T1~T6 RED (6)
└── boundary/            # U-T1~T6, U-GUI-01~04, D-ARC-03 RED (9)
```

논리 의존: `boundary → app → domain`. 상세: [`docs/PRD.md`](docs/PRD.md) §5.6, [`.cursorrules`](.cursorrules)

**pytest 현황:** `tests/` **8 passed, 15 failed** (GREEN 8 + RED 스켈레톤 15 — fail은 의도적)

---

## 기본 요구사항

### 입력·출력 (Phase 0 — 현재)

사용자 입력 예시:

```
meter:2.5
```

→ 출력 (3단위 전체, 하위 호환 AC1 — Golden baseline 고정):

```
2.5 meter = 8.2021 feet
2.5 meter = 2.5 meter
2.5 meter = 2.734025 yard
```

### 현재 구현 vs 로드맵

| 구분 | 내용 | 상태 |
|------|------|------|
| **아키텍처** | `unit_converter/` 레이어 분리 + AST 가드 (T5, A4) | ✅ Phase 0 GREEN |
| **CLI** | `meter:2.5` 3줄 출력 (AC1) | ✅ + Golden |
| **CLI** | `meters` 별칭, trim, 제안·목록 (F4, F6, F7) | 🔴 RED TC (Phase 1, 3~4) — 구현 대기 |
| **CLI** | `meter:2.5:yard` 목표 1줄 (F5, AC8) | 🔴 RED TC (Phase 2) — 구현 대기 |
| **GUI** | from/to 드롭다운 + 목표 1줄 (G1, G2, PyQt6) | 🔴 RED TC (Phase 5) — **실행 불가** |
| **공통** | CLI·GUI 동일 결과 (G4, AC12) | 🔴 RED TC (U-T6-01) — GUI 선행 |

**Mom Test 핵심 문제 (페르소나 B):** 단위명 오타(`meters`) → Unknown unit → 출력 확인 후 ~5분 재작업. 전체 3단위 출력 불필요, **목표 단위만** 필요한 경우가 자주 발생.

### 지원 단위

- meter
- feet
- yard

새 단위 추가 시 기존 코드 변경 최소화(OCP). 각 단위 간 변환은 테스트로 검증.

---

## 비즈니스 로직

- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간 비율은 meter 기반으로 계산 (계수 SSOT: `unit_converter/domain/unit_registry.py`)

---

## 품질 요구사항

- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)
- Dual Track TDD: Logic(`D-*`) / UI(`U-*`) — RED → GREEN → Golden → REFACTOR

### 아키텍처 (v0.2)

| 레이어 | 경로 | 역할 |
|--------|------|------|
| **entity** | `domain/` | 변환 비율·단위 (I/O 없음) |
| **control** | `app/` | 파싱·출력 문자열 (I/O 없음) |
| **boundary** | `cli.py`, (추후 `gui_boundary.py`) | `input()` / `print()` / PyQt6 |

---

## 추가 요구사항 (로드맵)

| 항목 | 버전 |
|------|------|
| OCP registry 전면 | v0.3 |
| 설정 외부화 (JSON/YAML), cubit 동적 등록 | v0.4 |
| 출력 포맷 선택 (JSON / CSV / 표) | v1.0 |

---

## 문서·보고서

| 경로 | 설명 |
|------|------|
| [`docs/PRD.md`](docs/PRD.md) | 제품 요구사항 (v0.2) |
| [`docs/UnitConverter_MomTest_Report.md`](docs/UnitConverter_MomTest_Report.md) | Mom Test 상세 |
| [`Reports/01_UnitConverter_ProblemDefinition_Report.md`](Reports/01_UnitConverter_ProblemDefinition_Report.md) | 코드 역분석 |
| [`Reports/02_UnitConverter_MomTest_Report.md`](Reports/02_UnitConverter_MomTest_Report.md) | Mom Test 요약 |
| [`Reports/03_UnitConverter_Boundary_GUI_Report.md`](Reports/03_UnitConverter_Boundary_GUI_Report.md) | Boundary·GUI Spec 보강 |
| [`Reports/04_UnitConverter_Architecture_Package_Report.md`](Reports/04_UnitConverter_Architecture_Package_Report.md) | 패키지 아키텍처·RED |
| [`Reports/05_UnitConverter_RED_Phase_Report.md`](Reports/05_UnitConverter_RED_Phase_Report.md) | RED 단계 (설계·스켈레톤·venv) |
| [`Reports/06_UnitConverter_GREEN-Golden_Phase_Report.md`](Reports/06_UnitConverter_GREEN-Golden_Phase_Report.md) | GREEN·Golden Master (Phase 0) |
| [`Reports/07_UnitConverter_RED_v0.2_Full-Phase_Report.md`](Reports/07_UnitConverter_RED_v0.2_Full-Phase_Report.md) | **RED v0.2 전 Phase (1~5 스켈레톤 15건)** |
| [`Prompts/01_UnitConverter_Spec-Export-Transcript.md`](Prompts/01_UnitConverter_Spec-Export-Transcript.md) | Spec Export Transcript |
| [`Prompts/02_UnitConverter_Boundary-GUI-Spec-Transcript.md`](Prompts/02_UnitConverter_Boundary-GUI-Spec-Transcript.md) | Boundary·GUI Transcript |
| [`Prompts/03_UnitConverter_Architecture-RED-Transcript.md`](Prompts/03_UnitConverter_Architecture-RED-Transcript.md) | Architecture·RED Transcript |
| [`Prompts/04_UnitConverter_RED-Phase-Transcript.md`](Prompts/04_UnitConverter_RED-Phase-Transcript.md) | RED Phase·venv Transcript |
| [`Prompts/05_UnitConverter_GREEN-Golden-Transcript.md`](Prompts/05_UnitConverter_GREEN-Golden-Transcript.md) | GREEN·Golden Transcript |
| [`Prompts/06_UnitConverter_RED-v0.2-Full-Phase-Transcript.md`](Prompts/06_UnitConverter_RED-v0.2-Full-Phase-Transcript.md) | **RED v0.2 전 Phase Transcript** |

---

## 생성형AI를 활용한 Activities (6 시간)

| 단계 | 내용 | 시간 |
|------|------|------|
| 문제 코드 및 기본 요구사항 분석 | 기본 코드구조, 로직 이해 | 0.5시간 |
| 기본 요구사항 및 품질 요구사항 구현 | OCP, SRP, **패키지 분리**, v0.2 Mom Test·GUI | 2시간 |
| TC 구현 | pytest Logic/UI, RED→GREEN, Golden, AC7·AC8·AC12 | 0.5시간 |
| 추가 요구사항 구현 | 설정 외부화, 출력 포맷 등 | 2시간 |
| 회고 및 발표 | 목표 달성도, AI 활용, TC·리팩터링 회고 | 1시간 |

### 회고 주제

- AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
- TC를 추가보면서 개선에 미친 영향, TC 작성 팁
- 클린코드와 리팩토링에서 느낀 장점과 어려운점
