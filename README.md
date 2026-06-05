# Unit Converter (Python)

작성자:이원준, 리뷰어:손효진, 이동규, 이정수, 이현지, 이현진

![unit-converter](./unit-converter.jpg)

## Overview

길이 단위(meter, feet, yard) 간 변환 프로그램. **CLI**와 **데스크톱 GUI**를 지원하며, 새 단위 추가 시 기존 코드 변경을 최소화하도록 설계한다. 변환 로직은 테스트 코드로 검증한다.

| 버전 | 상태 | 설명 |
|------|------|------|
| v0.1 | ✅ 현재 코드 | 단일 `main()`, 3단위 전체 출력 |
| **v0.2** | 📋 Spec 확정 | Mom Test 반영 + GUI + 최소 Boundary 분리 |
| v0.3~ | 로드맵 | OCP registry, 설정 외부화 등 — [`docs/PRD.md`](docs/PRD.md) §11 |

**상세 요구사항:** [`docs/PRD.md`](docs/PRD.md) · Mom Test: [`docs/UnitConverter_MomTest_Report.md`](docs/UnitConverter_MomTest_Report.md)

---

## 가상환경 설정 및 실행

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# CLI 실행 (현재)
python UnitConverter.py

# GUI 실행 (v0.2 목표 — 구현 예정)
# python -m gui   또는   python gui_boundary.py

# 가상환경 비활성화
deactivate
```

---

## 기본 요구사항

### 입력·출력 (v0.1 — 현재)

사용자 입력 예시:

```
meter:2.5
```

→ 출력 (현재: 3단위 전체):

```
2.5 meter = 2.5 meter
2.5 meter = 8.2021 feet
2.5 meter = 2.734025 yard
```

### v0.2 확장 (Mom Test + GUI — Spec)

| 구분 | 내용 |
|------|------|
| **CLI** | `meter:2.5:yard` — 목표 단위 1줄만 (F5) |
| **CLI** | `meters` 별칭, trim, 오류 시 제안·목록 (F4, F6, F7) |
| **GUI** | from/to 드롭다운 + 값 → 목표 단위 1줄 (G1, G2) |
| **공통** | CLI·GUI 동일 변환 결과 (G4, AC12) |

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
- feet/yard 간 비율은 meter 기반으로 계산

---

## 품질 요구사항

- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 아키텍처 (v0.2 목표 — Boundary / Control / Entity)

```
boundary (CLI / GUI) → parser / converter / presenter (control) → unit registry (entity)
```

| 레이어 | 역할 |
|--------|------|
| **entity** | 변환 비율·단위 정의 (I/O 없음) |
| **control** | 파싱, 검증, 변환, 출력 포맷 |
| **boundary** | `input()` / `print()` / Tkinter 등 진입점만 |

의존 방향: boundary → control → entity. 상세: [`docs/PRD.md`](docs/PRD.md) §5.6, [`.cursorrules`](.cursorrules)

---

## 추가 요구사항 (로드맵)

| 항목 | 버전 |
|------|------|
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
| [`Prompts/02_UnitConverter_Boundary-GUI-Spec-Transcript.md`](Prompts/02_UnitConverter_Boundary-GUI-Spec-Transcript.md) | Spec 세션 Transcript |

---

## 생성형AI를 활용한 Activities (6 시간)

| 단계 | 내용 | 시간 |
|------|------|------|
| 문제 코드 및 기본 요구사항 분석 | 기본 코드구조, 로직 이해 | 0.5시간 |
| 기본 요구사항 및 품질 요구사항 구현 | OCP, SRP, 입력 검증, **v0.2 Mom Test·GUI** | 2시간 |
| TC 구현 | 변환·검증 TC, AC7·AC8·AC12 | 0.5시간 |
| 추가 요구사항 구현 | 설정 외부화, 출력 포맷 등 | 2시간 |
| 회고 및 발표 | 목표 달성도, AI 활용, TC·리팩터링 회고 | 1시간 |

### 회고 주제

- AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
- TC를 추가보면서 개선에 미친 영향, TC 작성 팁
- 클린코드와 리팩토링에서 느낀 장점과 어려운점
