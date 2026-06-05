# UnitConverter — RED Test ID · C2C 참조

SSOT: `docs/PRD.md`, `.cursorrules`, `docs/UnitConverter_MomTest_Report.md`.

## ID 접두사

| 접두사 | Track | Layer | 파일 패턴 |
|--------|-------|-------|-----------|
| `D-*` | Logic | entity, control | `tests/entity/test_d_*.py`, `tests/control/test_d_*.py` |
| `U-*` | UI | boundary (CLI·GUI) | `tests/boundary/test_u_*.py` |

## PRD Tn → RED ID (시드)

| Tn | AC | PRD 요구 | Logic `D-*` (우선) | UI `U-*` (해당 시) |
|----|-----|----------|-------------------|-------------------|
| T1 | AC7, AC9 | F4, I6 — `meters` 별칭·trim | D-T1-01 `normalize_unit("meters")`→`meter` | U-T1-01 CLI `meters:2.5` 성공 또는 제안 |
| T2 | AC8 | F5, I2, O2 — `meter:2.5:yard` 1줄 | D-T2-01 `present(..., to=yard)` 1줄 | U-T2-01 CLI 출력 yard만 |
| T3 | AC1 | O1 하위 호환 3줄 | D-T3-01 `present` to 미지정 3줄 | — |
| T4 | S6 | F6,F7 — 즉시 피드백 | D-T4-01 unknown unit 메시지 구조 | U-T4-01 오류 후 5분 시나리오 회피 UX |
| T5 | AC11 | A1,A2 — control I/O 금지 | D-T5-01 import `parser` no print/input | — |
| T6 | AC12 | G4 — CLI·GUI 동일 | D-T6-01 동일 입력 동일 값 | U-T6-01 GUI=CLI 결과 |

## Phase → 권장 RED 묶음

| Phase | RED 묶음 예 |
|-------|-------------|
| 0 | D-T5-01, D-ARC-01 (모듈 골격 import) |
| 1 | D-T1-01 (+ U-T1-01 boundary는 Phase 1 후반) |
| 2 | D-T2-01, U-T2-01 |
| 5 | U-T6-01, U-GUI-01 |

## Invariant (Logic Track)

| ID | 내용 |
|----|------|
| I1 | meter 기준 정규화 (D1, D4) |
| I2 | 계수 3.28084 / 1.09361 — registry·상수 SSOT (CS5, CS6) |
| I3 | feet↔yard 직접 API 없음 — meter 경유 (PRD 비목표) |
| I4 | control에 `input`/`print`/tkinter 없음 (AC11) |
| I5 | 출력 포맷 일관 소수 (AC10, S9) |

## 픽스처 (로직만, Mock 아님)

| 이름 | 용도 |
|------|------|
| `G_meter_2_5` | `("meter", 2.5)` 또는 raw `"meter:2.5"` |
| `G_meters_typo` | `"meters:2.5"` |
| `G_to_yard` | `"meter:2.5:yard"` |
| `G_unknown_abc` | `"abc:1"` |

## Expected RED Failure (Logic)

| 상황 | 기대 실패 |
|------|-----------|
| 모듈 미생성 | `ModuleNotFoundError` |
| 동작 미구현 | `AssertionError` |
| 의도적 RED 마커 | `pytest.fail("RED: D-T1-01")` |

## UI/Boundary — Mock 정책 (Track UI)

- **허용:** control `parser`/`converter`/`presenter` 스텁·Mock
- **금지:** Logic Track에서 registry·converter Mock

## C2C 예시 (T1)

| 단계 | 내용 |
|------|------|
| PRD | F4, I6, AC7 — `meters`→`meter`; Unknown만 금지 |
| To-Do | `normalize_unit`이 `meters`를 허용한다 |
| Test | D-T1-01: Given `meters` → Then canonical `meter` |
