# UnitConverter PRD (Product Requirements Document)

| 항목 | 내용 |
|------|------|
| 제품 | UnitConverter — 길이 단위 변환 (CLI + GUI 계획) |
| 버전 | 0.2 (Mom Test + GUI) |
| 작성일 | 2026-06-05 |
| 상태 | Draft — Mom Test + GUI v0.2 범위 확정 |
| 소스 | [`UnitConverter.py`](../UnitConverter.py), [`README.md`](../README.md) |
| Mom Test | [`UnitConverter_MomTest_Report.md`](./UnitConverter_MomTest_Report.md) |

---

## 1. 배경

학습·실습 맥락에서 **길이 단위(meter, feet, yard)** 간 변환을 CLI로 수행하는 프로그램이다. 사용자는 `단위:값` 형식으로 입력하면 변환 결과를 터미널에 출력한다.

현재 [`UnitConverter.py`](../UnitConverter.py)는 **단일 파일·단일 함수** 구조의 초기 구현이다. **2026-06-05 Mom Test**(페르소나 B)에서 실무 사용(해외 메일 작성) 시 **단위 오타·전체 출력 불필요** 문제가 확인되어, v0.2 범위가 보강되었다.

**v0.2**에서 Mom Test 대응(**F4~F7**, P0)과 **GUI Boundary**(**G1~G5**)를 함께 구현한다. GUI는 드롭다운 선택으로 S3~S8을 직접 해소하고, CLI는 별칭·목표 단위로 동일 문제를 보완한다. 구현 시 **최소 Boundary / Control / Entity** 분리(A1~A5)로 CLI·GUI가 **동일 control**을 공유하며, 전면 OCP 리팩터는 v0.3으로 미룬다.

---

## 2. 목표

### 2.1 진짜 문제 (Problem Statement — Mom Test)

실무에서 **특정 단위 쌍**(예: meter→yard)만 필요할 때, CLI에 단위명을 **정확히 타이핑**해야 한다. **`meters` 오타**는 Unknown unit으로 실패하고, 사용자는 **출력을 본 뒤**야 알아채 **약 5분**을 다시 쓴다. 프로그램은 **세 단위를 모두** 출력하지만, 실제 필요는 **선택한 목표 단위**인 경우가 **자주** 있다.

| 증거 ID | 사실 |
|---------|------|
| S1 | 2026-06-05, meter→yard, 해외 발신 메일 |
| S4 | `meters` 오타 → Unknown unit |
| S6 | 재시도 ~5분 |
| S7·S8 | 전체 3단위 출력 불필요, 목표 단위 선택 필요 |

### 2.2 제품 목표 (한 문장)

**CLI**(`단위:값`, 목표 단위) 또는 **GUI**(from/to 선택 + 값)로 입력을 받아, **meter 기준 정규화** 후 **요청한 단위** 변환 결과를 출력하고, **오타·별칭·선택 UI**로 **5분 재작업 전**에 실패를 복구한다.

### 2.3 비목표 (Out of Scope — v0.2)

- **웹 인터페이스** (데스크톱 GUI는 v0.2 In Scope)
- JSON·CSV·표 형태 **출력 포맷 선택** (v1.0)
- **설정 파일(JSON/YAML)** 로드 (v0.4)
- **런타임 사용자 정의 단위** 등록 — cubit (v0.4)
- feet ↔ yard **직접 변환 API** (meter 경유 유지)

### 2.4 v0.2 In Scope (Mom Test + GUI)

**CLI (P0)**

- 단위 **별칭·정규화** (F4)
- **목표 단위 선택** 출력 (F5)
- Unknown unit **제안** (F6)
- 오류 시 **지원 단위 목록** (F7)

**GUI (P0)**

- from/to **선택 UI**, 목표 단위 **1줄** 출력 (G1, G2)
- CLI와 **동일 변환 결과** (G4), GUI **진입점** (G5)
- 오류 **인라인 피드백** (G3, P1)

**아키텍처 (v0.2 최소)**

- **최소** entity / control / CLI·GUI boundary 분리 (A1~A5) — GUI 구현 선행 조건
- pytest T1~T6, AC7~AC12

### 2.5 v0.3+ In Scope

- OCP **registry** 전면 도입, SRP 클래스 분리 강화
- CLI boundary 모듈 정리 (C3), AC11 정적 검사 강화

---

## 3. 사용자

| 페르소나 | 설명 | Mom Test |
|----------|------|----------|
| **A. 학습자** | Python CLI 실습, OCP/SRP·TC | (미인터뷰) |
| **B. 실무 변환 사용자** | 메일·문서 작성 시 **특정 단위 쌍** 필요; GUI에서 **드롭다운 선택**으로 오타 회피 기대 | **인터뷰 완료** |
| **C. 리뷰어** | 과제 채점·검증 | (미인터뷰) |

| 맥락 | 행동 |
|------|------|
| 해외 메일 | meter→yard **한 줄**만 필요 |
| CLI 실습 | `python UnitConverter.py` → `meter:2.5` |
| GUI (v0.2) | from/to 단위 선택 + 값 입력 → **목표 단위 1줄** 표시 |

---

## 4. 도메인 요구사항

### 4.1 지원 단위 및 변환 비율

| ID | 요구사항 | 우선순위 | 근거 |
|----|----------|----------|------|
| D1 | **meter** — 기준 단위 (1:1) | P0 | 코드 |
| D2 | **feet** — 1 meter = **3.28084** feet | P0 | README |
| D3 | **yard** — 1 meter = **1.09361** yard | P0 | README |
| D4 | feet·yard는 **meter 기준** 간접 계산 | P0 | 코드 |
| D5 | 출력값 **정확도** — 사용자가 프로그램 출력 **신뢰** (S9) | P0 | Mom Test |

### 4.2 입력 형식

| ID | 요구사항 | 우선순위 | 상태 |
|----|----------|----------|------|
| I1 | `{from_unit}:{value}` (예: `meter:2.5`) | P0 | ✅ 구현 |
| I2 | `{from_unit}:{value}:{to_unit}` — **목표 단위 선택** (F5) | P0 | ❌ v0.2 |
| I3 | `:` 미포함 → 오류 메시지 | P0 | ✅ |
| I4 | value **float** 파싱 | P0 | ✅ |
| I5 | 알 수 없는 unit → 오류 | P0 | ✅ |
| I6 | **별칭** `meters`→`meter`, **trim**, 대소문자 (F4) | P0 | ❌ v0.2 |

### 4.3 출력

| ID | 요구사항 | 우선순위 | 상태 |
|----|----------|----------|------|
| O1 | to_unit **미지정** → meter·feet·yard 각 1줄 (하위 호환) | P1 | ✅ |
| O2 | to_unit **지정** → **해당 단위 1줄만** (F5, S7) | P0 | ❌ v0.2 |
| O3 | `{value} {from_unit} = {converted} {to_unit}` | P0 | ✅ |
| O4 | **일관된 소수 표시** (AC10, S9) | P1 | ❌ |

---

## 5. 기능 요구사항

### 5.1 변환 (Core — 현재 구현)

| ID | 요구사항 | Mom Test | 상태 |
|----|----------|----------|------|
| F1 | 입력 unit → meter 기준값 | — | ✅ |
| F2 | meter 기준값 → (전체 또는 선택) 단위 | S7 | ⚠️ 전체만 |
| F3 | 형식·숫자·단위 오류 시 종료 | S4 | ✅ |

### 5.2 Mom Test 유도 (v0.2 — Core)

| ID | 요구사항 | Mom Test | 우선순위 |
|----|----------|----------|----------|
| F4 | 단위 **별칭·정규화** (`meters`→`meter`) | S3, S4, AC7 | P0 |
| F5 | **목표 단위 선택** 출력 | S7, S8, AC8 | P0 |
| F6 | Unknown unit → **유사 단위 제안** | S4, S6 | P0 |
| F7 | 오류 시 **지원 단위 목록** | S3 | P0 |

### 5.3 CLI Boundary (Command)

CLI 전용 **boundary** 요구사항. 변환·검증 로직은 control에 둔다 (A3).

| ID | 요구사항 | 우선순위 | 상태 |
|----|----------|----------|------|
| C1 | CLI 대화형 `input()` — boundary만 | P0 | ✅ |
| C2 | `if __name__ == "__main__":` CLI 진입점 | P0 | ✅ |
| C3 | CLI boundary **모듈 분리** (`cli_boundary` 등) | P1 | ❌ v0.2 |

### 5.4 검증

| ID | 요구사항 | 상태 |
|----|----------|------|
| V1 | `:` 형식 | ✅ |
| V2 | float 파싱 | ✅ |
| V3 | unit 화이트리스트 | ✅ |
| V4 | 음수 거부 | ❌ |
| V5 | trim·별칭 (F4) | ❌ v0.2 |
| V6 | 빈 unit/value | ❌ |

### 5.5 Test Loop

| ID | 요구사항 | Mom Test |
|----|----------|----------|
| T1 | **Red:** `meters:2.5` → Unknown (현재) / 별칭 성공 (목표) | AC7 |
| T2 | **Red:** `meter:2.5:yard` → yard 1줄만 | AC8 |
| T3 | **Green:** `meter:2.5` 전체 3줄 (하위 호환) | AC1 |
| T4 | 잘못된 입력 → **수 분 내** 로컬 피드백 (5분 재작업 전) | S6 |
| T5 | control import — `input`/`print`/GUI 프레임워크(`tkinter`, `PyQt6`) **없음** | AC11 |
| T6 | 동일 입력 — CLI·GUI **동일 변환 결과** | AC12 |

> T5는 v0.2 **최소 분리** 시 권장, v0.3에서 정적 검사 강화.

### 5.6 아키텍처 (패키지 레이아웃 + 논리 레이어)

[`.cursorrules`](../.cursorrules)와 동기화. **SSOT는 본 절.**

**물리 구조(고정)** — 소스 루트 `unit_converter/`:

```
unit_converter/
├── domain/                 # 논리: entity (A1)
│   ├── length_unit.py      # Protocol: name, to_meter() — v0.3 OCP 확장
│   ├── unit_registry.py    # 등록·조회 — v0.3 OCP 핵심; v0.2는 내장 3단위
│   └── converter.py        # meter 기준값 → 전 단위 (SRP, D4)
├── infrastructure/         # v0.4 설정 외부화
│   └── config_loader.py    # JSON/YAML — v0.4까지 스텁
├── app/                    # 논리: control (A2)
│   ├── input_parser.py     # PRD parser — I1~I6, F4(Phase 1+)
│   └── output_formatter.py # PRD presenter — O3; json|csv|table은 v1.0
├── cli.py                  # PRD CLI boundary (A3, C1~C2)
└── (gui_boundary.py)       # PRD GUI boundary (A5, G5) — v0.2 Phase 5

tests/
├── test_converter.py       # Domain / Logic Track (T3, D*)
└── test_cli.py             # Boundary / UI Track (AC1, C*)
```

**논리 의존(고정):**

```
boundary (cli / gui) → app (parser, presenter) → domain (registry, converter)
```

| ID | 요구사항 | 물리 위치 | 논리 레이어 | 우선순위 | 상태 |
|----|----------|-----------|-------------|----------|------|
| A1 | 변환 비율·단위 정의만; I/O·GUI **금지** | `domain/*` | entity | P0 | Phase 0 |
| A2 | 파싱·검증·출력 **문자열**; `input`/`print`/GUI 프레임워크(`tkinter`, `PyQt6`) **금지** | `app/*` | control | P0 | Phase 0 |
| A3 | `input()` / `print()` / **PyQt6 위젯** 등 **플랫폼 I/O만** | `cli.py`, `gui_*` | boundary | P0 | Phase 0 |
| A4 | **boundary → app → domain**; 역방향 import 금지 | 전체 | — | P0 | Phase 0 |
| A5 | CLI·GUI **독립 boundary**, **동일 app·domain** | `cli.py` + `gui_*` | boundary | P0 | Phase 5 |

**파일별 PRD 범위 (구현은 Phase·버전 준수):**

| 파일 | PRD 대응 | v0.2 | 이후 |
|------|----------|------|------|
| `length_unit.py` | D1~D4, OCP 단위 계약 | 내장 3단위 Protocol/타입 | v0.3 클래스·등록 |
| `unit_registry.py` | D1~D3, CS3·CS5 | `meter`/`feet`/`yard` 조회 | v0.3 OCP registry |
| `converter.py` | F1~F2, D4 | meter↔전 단위 | F5 to_unit 필터(Phase 2) |
| `input_parser.py` | I1~I6, F4 | `from:value` (Phase 0); 별칭·trim(Phase 1) | `from:value:to`(Phase 2) |
| `output_formatter.py` | O3, presenter(AC11) | **table** 3줄/1줄 문자열 | v1.0 json\|csv\|table |
| `config_loader.py` | §2.3, §11 v0.4 | **미구현 스텁** | JSON/YAML |
| `cli.py` | C1~C2, A3 | 대화형 CLI | C3 모듈 정리(P1) |

**역할 구분:** `output_formatter.py` = PRD **presenter**. 터미널·위젯 I/O는 **boundary**만.

**하위 호환:** [`UnitConverter.py`](../UnitConverter.py)는 `python -m unit_converter.cli` 또는 `cli.main()` 위임 진입점.

### 5.7 GUI Boundary (v0.2)

Mom Test S3~S8의 **주요 해소 수단**. F4~F7(P0)과 **병행** — CLI 하위 호환·학습용. 변환 로직은 control에 위임 (A2, A5).

**GUI 기술 스택:** **PyQt6** (Tkinter **미사용**). 위젯·이벤트·레이아웃은 `gui_boundary`에만 두고, `app`/`domain`은 PyQt6 import **금지** (AC11).

| ID | 요구사항 | Mom Test | 우선순위 | 상태 |
|----|----------|----------|----------|------|
| G1 | from / to 단위 **선택 UI** (드롭다운 등) — 단위명 **오타 방지** | S3, S4, F4, F6 | P0 | ❌ v0.2 |
| G2 | **목표 단위 1개** 결과만 표시 (전체 3단위 기본 출력 금지) | S7, S8, F5 | P0 | ❌ v0.2 |
| G3 | 오류 시 **인라인 피드백** (지원 단위·제안) | F7, S6 | P1 | ❌ v0.2 |
| G4 | CLI와 **동일 변환 결과** — AC1~AC10 공유 | S9, D5 | P0 | ❌ v0.2 |
| G5 | GUI 진입점 분리 (예: `python -m unit_converter.gui` 또는 `gui_boundary.py`) — **PyQt6** | A5 | P0 | ❌ v0.2 |

---

## 6. 성공 기준 (Acceptance)

| ID | Given | When | Then |
|----|-------|------|------|
| AC1 | `meter:2.5` | convert | meter·feet·yard 3줄 (하위 호환) |
| AC2 | `feet:3.28084` | convert | meter ≈ 1.0 |
| AC3 | `yard:1.09361` | convert | meter ≈ 1.0 |
| AC4 | `abc:1` | convert | 오류 + (v0.2) 지원 목록·제안 |
| AC5 | `meter:abc` | convert | `Invalid number` |
| AC6 | `meter2.5` | convert | 형식 오류 |
| **AC7** | `meters:2.5` | convert | **성공 또는 meter 제안** — Unknown만 금지 (S4) |
| **AC8** | meter→yard 메일 작성 | `meter:2.5:yard` | **yard 1줄만** (S7) |
| **AC9** | ` meter : 2.5 ` | convert | 정상 (trim) |
| **AC10** | 변환 성공 | 출력 | 신뢰 가능한 **일관 소수** (S9) |
| **AC11** | app 모듈 (`input_parser`, `output_formatter`)·`domain/*` | import·정적 검사 | `input`, `print`, GUI 프레임워크(`tkinter`, `PyQt6`) **없음** (A1, A2) |
| **AC12** | `meter:2.5:yard` 동일 의미 입력 | CLI convert / GUI convert | **동일** 변환값·포맷 (G4) |

---

## 7. R-G-I-O 요약

| | |
|--|--|
| **Role** | 실무·학습 사용자 (CLI 또는 GUI) |
| **Goal** | 필요 **단위 쌍**만 빠르게 확인, 오타 **즉시 복구** |
| **Input** | CLI: `from:value` 또는 `from:value:to` / GUI: from·to 선택 + 값 |
| **Output** | 선택 단위 1줄 (또는 전체 모드 3줄); boundary는 표시만, 로직은 control |

---

## 8. README 대비 갭

| 구분 | README | 목표 버전 |
|------|--------|-----------|
| Mom Test | — | v0.2 — F4~F7 (P0), AC7~AC10 |
| GUI | (명시 없음) | v0.2 — §5.7, G1~G5, AC12 |
| Boundary 최소 분리 | (명시 없음) | v0.2 — §5.6 A1~A5 |
| OCP/SRP 전면 | registry, 클래스 분리 | v0.3 — C3, AC11 강화 |
| TC | pytest | v0.2 — T1~T6 |
| 설정 외부화 | JSON/YAML | v0.4 |
| 출력 포맷 | JSON/CSV/표 | v1.0 |

---

## 9. 코드 스멜 분석

[`UnitConverter.py`](../UnitConverter.py) 기준. Mom Test로 **검증된** 항목은 표시.

| ID | 스멜 | Mom Test | 영향 |
|----|------|----------|------|
| CS3 | OCP 위반 — if-elif | — | 단위 추가 시 main 수정 |
| CS4 | 테스트 불가 — I/O in main | — | TC 곤란 |
| CS5 | Magic Number | — | 3.28084, 1.09361 |
| CS6 | 중복 변환 로직 | — | 입력·출력 이중 |
| **CS9** | No trim | **S3, S4** | ` meter ` 실패 |
| **CS10** | Primitive Obsession | **S4 (`meters`)** | Unknown unit, ~5분 |
| **CS14** | Hard-coded 3줄 출력 | **S7, S8** | 불필요 출력 |
| CS8 | 음수 미검증 | — | README 갭 |
| CS13 | Raw float | **S9** | 신뢰 저하 가능 |

**v0.2 우선:** CS10, CS14, CS9 → F4, F5, G1, G2; CS4 → A1~A5 최소 분리

---

## 10. 리스크·공백

| 항목 | 내용 | 완화 |
|------|------|------|
| 단일 Mom Test | 페르소나 B 1회 | A·C 추가 인터뷰 |
| 하위 호환 | 전체 3줄 vs 선택 1줄 | to_unit 생략 시 3줄 유지 |
| 5분 재작업 | 1회 추정 | AC7 TC |
| Boundary 미분리 | GUI 추가 시 main에 PyQt6 결합 (CS4) | v0.2 **A1~A5 최소 분리** 선행; PyQt6는 `gui_boundary`만 |
| CLI·GUI 결과 불일치 | 이중 로직·포맷 분기 | G4, AC12, 공유 control/presenter |
| F4~F7 vs GUI 중복 | 동일 Mom Test를 CLI·GUI 양쪽으로 해결 | F4~F7 P0 유지(CLI·TC), GUI는 G1~G2 P0 |

---

## 11. 로드맵

| 단계 | 내용 |
|------|------|
| v0.1 | 단일 main, 3단위, 전체 출력 (현재 코드) |
| **v0.2** | **Mom Test + GUI** — F4~F7 (P0), G1~G5, **A1~A5 최소 분리**, AC7~AC12, pytest T1~T6 |
| **v0.3** | OCP registry 전면, SRP 강화, C3, T5·AC11 정적 검사 |
| v0.4 | 설정 외부화, cubit 동적 등록 |
| v1.0 | JSON/CSV/표 출력 |

---

## 12. 참고

- 문제 정의 보고서: [`Reports/01_UnitConverter_ProblemDefinition_Report.md`](../Reports/01_UnitConverter_ProblemDefinition_Report.md)
- Mom Test 보고서: [`Reports/02_UnitConverter_MomTest_Report.md`](../Reports/02_UnitConverter_MomTest_Report.md)
- Mom Test 상세: [`UnitConverter_MomTest_Report.md`](./UnitConverter_MomTest_Report.md)
- Boundary·GUI 보고서: [`Reports/03_UnitConverter_Boundary_GUI_Report.md`](../Reports/03_UnitConverter_Boundary_GUI_Report.md)
- 패키지·RED 보고서: [`Reports/04_UnitConverter_Architecture_Package_Report.md`](../Reports/04_UnitConverter_Architecture_Package_Report.md), [`05_UnitConverter_RED_Phase_Report.md`](../Reports/05_UnitConverter_RED_Phase_Report.md), [`06_UnitConverter_GREEN-Golden_Phase_Report.md`](../Reports/06_UnitConverter_GREEN-Golden_Phase_Report.md)
- Prompt Transcript: [`Prompts/01_UnitConverter_Spec-Export-Transcript.md`](../Prompts/01_UnitConverter_Spec-Export-Transcript.md), [`02_UnitConverter_Boundary-GUI-Spec-Transcript.md`](../Prompts/02_UnitConverter_Boundary-GUI-Spec-Transcript.md), [`03_UnitConverter_Architecture-RED-Transcript.md`](../Prompts/03_UnitConverter_Architecture-RED-Transcript.md), [`04_UnitConverter_RED-Phase-Transcript.md`](../Prompts/04_UnitConverter_RED-Phase-Transcript.md), [`05_UnitConverter_GREEN-Golden-Transcript.md`](../Prompts/05_UnitConverter_GREEN-Golden-Transcript.md)
- 개발 환경: `venv/` (없으면 생성) + [`requirements.txt`](../requirements.txt) (`PyQt6` 포함) — [`.cursorrules`](../.cursorrules) § 가상환경
- 실행: [`UnitConverter.py`](../UnitConverter.py), [`python -m unit_converter.cli`](../unit_converter/cli.py)
- 실습: [`README.md`](../README.md)
- Cursor 규칙: [`.cursorrules`](../.cursorrules)
