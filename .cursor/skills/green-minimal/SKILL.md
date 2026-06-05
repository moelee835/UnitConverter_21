---
name: green-minimal
description: >-
  UnitConverter ARRR Respond 단계 최소 GREEN. /green-minimal,
  RED Test ID 하나, pytest.fail 제거·assert 전환, entity/control/boundary
  최소 구현, constants SSOT, REFACTOR·다른 ID 동시 해결 금지.
disable-model-invocation: true
---

# GREEN Minimal (ARRR — Respond)

`/red-skeleton`으로 **FAILED** 확인된 **Test ID 하나**만 최소 구현으로 **PASSED**.

SSOT: [`.cursorrules`](../../../.cursorrules), [red-test-plan/reference.md](../red-test-plan/reference.md), [reference.md](reference.md).

## 선행 조건

- `tests/`에 해당 ID RED 스켈레톤 존재 (`pytest.fail` 또는 FAIL)
- C2C·설계표의 Given/When/Then 확정

## 언제 사용

| 트리거 | 예 |
|--------|-----|
| `/green-minimal` | D-T1-01 하나 GREEN |
| `Phase: green` | Respond · Delivery |

**사용하지 않을 때:** REFACTOR, 다른 Test ID 동시 GREEN, assert 완화·skip·xfail, git commit(사용자 요청 전).

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity|control|boundary | Track: Logic|UI
RED 대상: D-T1-01 (tests/control/test_d_t1_01.py)
```

## 절차 (5단계)

### 1. RED 재확인

```bash
python -m pytest <해당 테스트 노드> -v
```

- **FAILED** (`pytest.fail` / `ModuleNotFoundError` / `AssertionError`) 확인
- 이미 **PASSED**면 스켈레톤 누락·범위 오류 — 중단·보고

### 2. 최소 구현 (이번 ID만)

| Layer | 경로 | 원칙 |
|-------|------|------|
| entity | `entity/constants.py`, `entity/unit_registry.py` | 계수·단위 SSOT; **매직넘버·하드코딩 금지** |
| control | `control/parser.py` 등 | Red 대상 **함수만**; 순수 함수 우선 |
| boundary | `boundary/cli_boundary.py` 등 | I/O만; 로직은 control 위임 |

- **`src/` 사용 안 함** — 루트 `entity/`, `control/`, `boundary/` (reference.md)
- **ECB:** `boundary → control → entity`; entity·control이 boundary import **금지**
- **I/O 금지 (entity·control):** `input`, `print`, `tkinter` (AC11, T5)
- **오류:** boundary/control 역할 분리 — entity에 사용자 메시지·CLI 오류 처리 넣지 않음 (MagicSquare E001~E005에 해당하는 **entity 처리 금지**와 동일 취지)

### 3. 스켈레톤 → assert

- `pytest.fail("RED: …")` **제거**
- When에 **실제 import·호출** 추가
- Then에 설계표 기대값 **assert** (완화·`approx` 남용 금지, AC10 시 정책 명시)

```python
from control.parser import normalize_unit

def test_d_t1_01_meters_alias_to_meter(g_meters_typo: str) -> None:
    # Given: "meters" 별칭
    # When:
    result = normalize_unit("meters")
    # Then:
    assert result == "meter"
```

### 4. PASS 확인

```bash
python -m pytest tests/control/test_d_t1_01.py::test_d_t1_01_meters_alias_to_meter -v
python -m pytest tests/control/test_d_t1_01.py -v
```

- 해당 파일 **전부 passed**
- **회귀 실패** 시 즉시 수정 또는 범위 롤백 보고

### 5. (선택) REPL 스모크

- Given 픽스처와 Then을 1~2줄로 재현 (예: `normalize_unit("meters") == "meter"`)
- 필수 아님 — 보고에 한 줄만

## GREEN 보고 템플릿

```markdown
## GREEN Minimal 보고

- **선언:** Phase: green | Layer: control | Track: Logic
- **Test ID:** D-T1-01 — PASSED
- **pytest:** 단일 노드 + 파일 스위트 passed
- **변경 파일:** tests/control/test_d_t1_01.py, control/parser.py, entity/constants.py (해당만)
- **회귀:** 없음 / (있으면 수정 내역)
- **다음:** REFACTOR는 별도 턴 · 다음 RED ID는 /red-skeleton
```

완료 한 줄: `GREEN 완료 — D-T1-01 PASSED. REFACTOR·다른 ID는 별도 요청.`

## 금지

| 금지 | |
|------|--|
| 이번 RED 묶음 **외** Test ID 동시 해결 | |
| REFACTOR (이름 정리·전면 OCP) | GREEN 턴 |
| assert 완화 · skip · xfail | |
| `UnitConverter.py` main() 대규모 이전 (범위 밖) | |
| git commit | 사용자 요청 시만 |

## ARRR 위치

| 단계 | Command |
|------|---------|
| Ask · 설계 | `/red-test-plan` |
| Ask · 골격 | `/red-skeleton` |
| **Respond · 최소 구현** | **`/green-minimal`** |
| **Respond · Golden** | [`/golden-master`](../golden-master/SKILL.md) (PASS 후) |
| Refactor · 스멜 분석 | [`/refactor-smell`](../refactor-smell/SKILL.md) |
| Refactor · 안전 적용 | [`/refactor-safe`](../refactor-safe/SKILL.md) |
