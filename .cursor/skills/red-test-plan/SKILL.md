---
name: red-test-plan
description: >-
  UnitConverter ARRR Ask 단계 RED 설계·C2C 추적(PRD→To-Do→Test Case).
  /red-test-plan, RED 설계표, T1~T6, D-*/U-* ID, Phase red, Logic/UI Track,
  구현·테스트 파일 생성 없이 계획만 할 때 사용.
disable-model-invocation: true
---

# RED Test Plan (ARRR — Ask)

Dual Track **Discovery / Ask**: ①기획 → ②설계 → ③RED 설계. **코드·테스트 파일 생성 없음.**

SSOT: [`.cursorrules`](../../../.cursorrules), [`docs/PRD.md`](../../../docs/PRD.md), [`docs/UnitConverter_MomTest_Report.md`](../../../docs/UnitConverter_MomTest_Report.md).  
ID·Tn 매핑: [reference.md](reference.md).

## 언제 사용

| 트리거 | 예 |
|--------|-----|
| `/red-test-plan` | RED 묶음 설계표·C2C·테스트 플랜만 |
| Ask 모드 | 구현 전 AC·Tn 정렬 |
| 다음 단계 안내 | 완료 후 [`/red-skeleton`](../red-skeleton/SKILL.md) (테스트 골격) |

**사용하지 않을 때:** GREEN/REFACTOR, `tests/`·`src/`·모듈 파일 생성, pytest 실행으로 통과시키기.

## C2C 규칙 (Rule 1~3)

1. **Rule 1 — 판단만 To-Do:** PRD에서 “허용한다/보인다/금지한다/해야 한다” 등 **판단·정책**만 To-Do. “파일을 연다”, “pytest를 실행한다” 등 단순 행동은 **폐기**.
2. **Rule 2 — 1:1:** To-Do 1개 ↔ Test Case 1개 (`D-*` 또는 `U-*`). 복합 요구는 **분해**.
3. **Rule 3 — RED 먼저:** 설계표의 모든 케이스는 **현재 FAIL/ERROR** 전제. GREEN·구현은 다음 Phase.

## RED 단계 절대 금지

- 구현 코드 작성 · GREEN · REFACTOR
- 모든 테스트는 **실패(FAIL/ERROR)** 상태로만 기술
- 의도적 RED 표현: `pytest.fail("RED: [Test ID]")` 한 줄 (설계 단계에서는 표에 기재)
- **Logic Track:** Domain(registry·converter) **Mock 금지** — 픽스처·실제 import만
- **UI Track:** control Mock **허용** (boundary만)
- `skip` / `xfail` / assert 완화 **금지**

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: entity|control|boundary | Track: Logic|UI
```

- `이번 RED 묶음: D-T1-01 (PRD F4, T1, AC7)` 형태로 범위 명시
- 한 턴 **RED 묶음 1~3개 Test ID** 권장

## 워크플로 (①②③)

### ① 기획

- PRD §4~§6, Mom Test S1~S9에서 **이번 묶음** 요구 인용 (ID: F4, I6, AC7, T1 등)
- v0.2 Phase 표(`.cursorrules`)와 충돌 없는지 확인
- “전 단위 3줄 기본 UX” 금지 여부 점검 (S7, S8)

### ② 설계

- 대상 **함수/모듈** 후보: `parser`, `converter`, `presenter`, `unit_registry` (아직 없으면 **이름만**)
- Layer·Track 확정: Logic → `D-*` / UI → `U-*`
- [reference.md](reference.md)에서 기존 ID와 중복 없게 ID 부여

### ③ RED 설계

아래 **두 표를 우선** 작성 (해당 Track만 있으면 하나만).

**UI/Boundary RED 설계표 (Track UI, `U-*`)**

| Test ID | Given | Then (기대값) | Expected RED Failure |
|---------|-------|---------------|----------------------|
| U-… | … | … | ModuleNotFoundError / AssertionError / pytest.fail RED |

**Domain/Logic RED 설계표 (Track Logic, `D-*`)**

| Test ID | 대상 함수 | Given→Then | Invariant | Expected RED Failure |
|---------|-----------|------------|-----------|----------------------|
| D-… | … | … | I1~I5 | … |

## 출력 템플릿 (4섹션)

`/red-test-plan` Command와 동일. 순서:

1. **C2C 추적** — PRD 인용 | To-Do 1개(판단) | Test ID → Given/When/Then  
2. **RED 설계표** — Track B `D-*` 및/또는 Track UI `U-*`  
3. **테스트 플랜** — 파일 경로, `test_*` 함수명, conftest 픽스처(로직만), pytest 명령, RED 묶음 범위  
4. **ECB·Mock 점검** — Logic Mock 금지, boundary는 user 메시지·I/O, control에 print/input 없음(T5)

## 완료 문장

설계 출력 끝에 **한 줄**:

`RED 설계 완료 — /red-skeleton 으로 테스트 골격 생성 가능.`

## Layer · Track 빠른 선택

| Layer | Track | 표 | 모듈(목표) |
|-------|-------|-----|------------|
| entity | Logic | D-* | `unit_registry`, 상수 SSOT |
| control | Logic | D-* | `parser`, `converter`, `presenter` |
| boundary | UI | U-* | `cli_boundary`, `gui_boundary` |

## 금지 요약

| 금지 | |
|------|--|
| `tests/`, `src/`, `*.py` 생성·수정 | Ask=설계만 |
| GREEN / REFACTOR | |
| Logic Track Domain Mock | |
| skip / xfail / assert 완화 | |
