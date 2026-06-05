# Unit Converter (Python)

작성자:이원준, 리뷰어:손효진, 이동규, 이정수, 이현지, 이현진

![unit-converter](./unit-converter.jpg)

## Overview

길이 단위(meter, feet, yard, cubit 등) 간 변환 프로그램. **CLI**와 **데스크톱 GUI**를 지원하며, 단위·계수는 **`config/units.json`** 으로 외부화하고 새 단위 추가 시 기존 코드 변경을 최소화하도록 설계한다. 변환 로직은 테스트 코드로 검증한다.

| 버전 | 상태 | 설명 |
|------|------|------|
| v0.1 | ✅ 하위 호환 | `UnitConverter.py` 진입점 유지 |
| **v0.2** | ✅ **GREEN 완료** | F4~F7 CLI + G1~G5 GUI + Golden — Report 08 |
| **Refactor** | ✅ **완료** | Sprint A~D — config SSOT, presenter, cubit, json/csv — **pytest 31 passed** — Report 09 |
| v0.3~ | 로드맵 | OCP registry 전면 등 — [`docs/PRD.md`](docs/PRD.md) §11 |

**상세 요구사항:** [`docs/PRD.md`](docs/PRD.md) · Mom Test: [`docs/UnitConverter_MomTest_Report.md`](docs/UnitConverter_MomTest_Report.md) · 개선: [`docs/Improvement_Roadmap.md`](docs/Improvement_Roadmap.md)

---

## 가상환경 · 의존성

의존성은 [`requirements.txt`](requirements.txt)로 관리합니다. 실행·테스트는 **venv 인터프리터만** 사용 ([`.cursorrules`](.cursorrules) § 가상환경).

```bash
# 1) venv 없으면 생성 (프로젝트 루트)
python -m venv venv

# 2) 활성화 (Windows)
venv\Scripts\activate

# 3) 의존성 설치 (SSOT: requirements.txt)
pip install -r requirements.txt

# CLI (권장)
python -m unit_converter.cli

# GUI (PyQt6)
python -m unit_converter.gui

# Windows: 활성화 없이 직접 호출
venv\Scripts\python.exe -m unit_converter.cli
venv\Scripts\python.exe -m unit_converter.gui
venv\Scripts\python.exe -m pytest tests/ -v

# 하위 호환
python UnitConverter.py

# 전체 테스트 (31 passed)
venv\Scripts\python.exe -m pytest tests/ -v

deactivate
```

새 패키지가 필요하면 `requirements.txt`에 추가한 뒤 `pip install -r requirements.txt`를 다시 실행합니다.

---

## 프로젝트 구조

```
config/
└── units.json             # 단위·계수·별칭·suggest_cutoff SSOT

unit_converter/
├── domain/                # entity — registry, converter, errors, length_unit
├── app/                   # control — input_parser, output_formatter, conversion_flow
├── infrastructure/        # config_loader — JSON 로드, create_default_registry()
├── cli.py                 # boundary — CLI (composition root)
├── gui_boundary.py        # boundary — PyQt6 GUI (G1~G5)
└── gui.py                 # boundary — python -m unit_converter.gui

tests/
├── test_converter.py      # Domain / Logic
├── test_cli.py            # Boundary / UI + Golden
├── _approval.py           # Golden Master 헬퍼
├── ast_helpers.py         # 아키텍처 AST 가드 (T5, A4)
├── golden/                # *.approved.txt baseline
├── conftest.py
├── entity/                # D-ARC-01, D-CUBIT-01
├── control/               # D-T1~T6, D-T4-03, D-O1, D-T5-01, D-ARC-02
└── boundary/              # U-T1~T6, U-GUI-01~04, D-ARC-03
```

논리 의존: `boundary → app → domain`. 설정: `config/units.json → infrastructure/config_loader → domain/unit_registry`. 상세: [`docs/PRD.md`](docs/PRD.md) §5.6

**pytest 현황:** `tests/` **31 passed**

---

## 기본 요구사항

### 입력·출력 예시

**하위 호환 (AC1) — `meter:2.5` (등록 단위 전체, table):**

```
2.5 meter = 4.770996 cubit
2.5 meter = 8.2021 feet
2.5 meter = 2.5 meter
2.5 meter = 2.734025 yard
```

**별칭 (F4) — `meters:2.5`:** 별칭 정규화 후 위와 동일 (별칭은 `config/units.json` → `aliases`)

**목표 1줄 (F5, AC8) — `meter:2.5:yard`:**

```
2.5 meter = 2.734025 yard
```

**JSON (v1.0) — `meter:2.5:yard:json`:**

```json
{"source":{"unit":"meter","value":2.5},"conversions":[{"unit":"yard","value":2.734025}]}
```

**CSV (v1.0) — `meter:2.5:csv`:**

```
from_unit,from_value,to_unit,to_value
meter,2.5,cubit,4.770996
meter,2.5,feet,8.2021
...
```

**음수 거부 (CS8) — `meter:-2.5`:** `Invalid number: negative values are not supported`

**GUI:** From/To 드롭다운(registry SSOT) → Value → Convert → Result 1줄. 오류 시 Error 영역에 지원 목록·제안 표시.

### 현재 구현 vs 로드맵

| 구분 | 내용 | 상태 |
|------|------|------|
| **아키텍처** | ECB + AST 가드 (T5, A4, D-ARC-03) | ✅ |
| **CLI** | `meter:2.5` 전체 단위 출력 (AC1) | ✅ + Golden |
| **CLI** | `meters` 별칭, trim, 제안·목록 (F4, F6, F7) | ✅ + Golden |
| **CLI** | `meter:2.5:yard` 목표 1줄 (F5, AC8) | ✅ + Golden |
| **CLI/GUI** | json / csv / table 출력 선택 | ✅ |
| **GUI** | from/to 드롭다운 + 목표 1줄 (G1, G2) | ✅ |
| **공통** | CLI·GUI 동일 결과 (G4, AC12) | ✅ |
| **Config** | `config/units.json` SSOT | ✅ |
| **Config** | cubit + `UnitRegistry.register()` | ✅ |
| **품질** | AC10 일관 소수, 음수 검증 | ✅ |

**Mom Test 핵심 문제 (페르소나 B):** 단위명 오타(`meters`) → Unknown unit → ~5분 재작업. **별칭·제안·GUI 드롭다운·목표 1줄**로 대응.

### 지원 단위

`config/units.json`에 정의 (기본):

| 단위 | 비고 |
|------|------|
| meter | 기준 |
| feet | |
| yard | |
| cubit | config 등록 (≈0.524 m) |

새 단위는 JSON에 항목 추가 또는 `UnitRegistry.register()`로 확장. GUI·CLI는 registry SSOT를 자동 반영.

---

## 비즈니스 로직

- 모든 변환은 **meter 기준 정규화** 후 대상 단위로 환산
- 계수 SSOT: [`config/units.json`](config/units.json) → [`unit_converter/domain/unit_registry.py`](unit_converter/domain/unit_registry.py)
- 출력 소수 정책: `DISPLAY_PRECISION = 6` ([`output_formatter.py`](unit_converter/app/output_formatter.py))

---

## 품질 요구사항

- OCP를 만족하는 설계 (Registry + config + `register()`)
- SRP를 만족하는 클래스 구성 (parser / presenter / domain 분리)
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)
- Dual Track TDD: Logic(`D-*`) / UI(`U-*`) — RED → GREEN → Golden → REFACTOR

### 아키텍처

| 레이어 | 경로 | 역할 |
|--------|------|------|
| **entity** | `domain/` | 변환·단위·예외 (I/O·UX 문자열 없음) |
| **control** | `app/` | 파싱·출력 문자열 presenter (I/O 없음) |
| **boundary** | `cli.py`, `gui_boundary.py` | `input()` / `print()` / PyQt6, composition root |
| **infrastructure** | `infrastructure/` | JSON config 로드 |

---

## 추가 요구사항 (로드맵)

| 항목 | 버전 | 상태 |
|------|------|------|
| 설정 외부화 (JSON), cubit | v0.4 | ✅ |
| 출력 포맷 (JSON / CSV / table) | v1.0 | ✅ |
| OCP registry 전면 | v0.3 | 로드맵 |

---

## 문서·보고서

| 경로 | 설명 |
|------|------|
| [`docs/PRD.md`](docs/PRD.md) | 제품 요구사항 |
| [`docs/Improvement_Roadmap.md`](docs/Improvement_Roadmap.md) | Sprint A~D 개선 로드맵 (완료) |
| [`docs/Code_smell.md`](docs/Code_smell.md) | 코드 스멜·리팩터링 기법 매핑 |
| [`docs/UnitConverter_MomTest_Report.md`](docs/UnitConverter_MomTest_Report.md) | Mom Test 상세 |
| [`Reports/08_UnitConverter_GREEN-Golden_v0.2_Full-Phase_Report.md`](Reports/08_UnitConverter_GREEN-Golden_v0.2_Full-Phase_Report.md) | GREEN·Golden v0.2 (23 passed) |
| [`Reports/09_UnitConverter_Refactor-Improvement_Report.md`](Reports/09_UnitConverter_Refactor-Improvement_Report.md) | **Refactor·Improvement (31 passed)** |
| [`Prompts/07_UnitConverter_GREEN-Golden-v0.2-Full-Phase-Transcript.md`](Prompts/07_UnitConverter_GREEN-Golden-v0.2-Full-Phase-Transcript.md) | GREEN·Golden Transcript |
| [`Prompts/08_UnitConverter_Refactor-Improvement-Transcript.md`](Prompts/08_UnitConverter_Refactor-Improvement-Transcript.md) | **Refactor·Improvement Transcript** |

이전 Reports·Prompts (01~07): [`Reports/`](Reports/) · [`Prompts/`](Prompts/)

---

## 생성형AI를 활용한 Activities (6 시간)

| 단계 | 내용 | 시간 |
|------|------|------|
| 문제 코드 및 기본 요구사항 분석 | 기본 코드구조, 로직 이해 | 0.5시간 |
| 기본 요구사항 및 품질 요구사항 구현 | OCP, SRP, 패키지 분리, v0.2 Mom Test·GUI | 2시간 |
| TC 구현 | pytest Logic/UI, RED→GREEN, Golden | 0.5시간 |
| 추가 요구사항 구현 | **config SSOT, json/csv 출력, cubit, refactor** | 2시간 |
| 회고 및 발표 | 목표 달성도, AI 활용, TC·리팩터링 회고 | 1시간 |

### 회고 주제

- AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
- TC를 추가보면서 개선에 미친 영향, TC 작성 팁
- 클린코드와 리팩토링에서 느낀 장점과 어려운점
