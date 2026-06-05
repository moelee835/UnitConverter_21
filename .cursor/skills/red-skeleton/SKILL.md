---
name: red-skeleton
description: >-
  UnitConverter ARRR Ask·Delivery RED 스켈레톤 작성. /red-skeleton,
  /red-test-plan 설계표 기준 tests/ 골격, pytest.fail RED, AAA 주석,
  tests/만 변경, src/·구현 금지, pytest FAIL 확인 후 보고.
disable-model-invocation: true
---

# RED Skeleton (ARRR — Ask → Delivery 경계)

`/red-test-plan`으로 확정한 **RED 설계표**를 `tests/` **스켈레톤 코드**로 옮긴다. **구현(GREEN) 없음.**

SSOT: [`.cursorrules`](../../../.cursorrules), [red-test-plan/reference.md](../red-test-plan/reference.md), [reference.md](reference.md).

## 선행 조건

- Test ID·Given/When/Then·파일 경로가 **이미 확정** (`/red-test-plan` 출력 또는 사용자 지정)
- 없으면 `/red-test-plan` 먼저 안내

## 언제 사용

| 트리거 | 예 |
|--------|-----|
| `/red-skeleton` | `tests/` + `conftest` RED 골격 |
| `pytest.fail("RED: D-T1-01")` | 의도적 실패만 |
| 설계표 → 코드 | C2C의 Test Case 구현(골격) |

**사용하지 않을 때:** `src/`·`entity/`·`control/`·`boundary/` **구현 모듈** 생성, assert로 통과, GREEN/REFACTOR.

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: entity|control|boundary | Track: Logic|UI
Test ID: D-T1-01
```

## 스켈레톤 규칙

| 규칙 | 내용 |
|------|------|
| AAA | `# Given:` / `# When:` / `# Then:` 주석 3줄 |
| Then | **`pytest.fail("RED: <Test ID> — …")` 한 줄만** — assert 본문·통과 더미 금지 |
| When | **주석만** — 대상 함수 호출은 GREEN까지 미작성 (import로 Red 깨지 않게) |
| Given | 픽스처 인자 또는 주석; Logic Track **Domain Mock 금지** |
| 파일 | `tests/`·`tests/conftest.py` **만** diff |
| 상수 | 계수는 **픽스처 데이터 조립 시만** `entity.constants` import; 모듈 없으면 입력 문자열 픽스처만 |
| 금지 | skip · xfail · `assert True` · 빈 pass |

## Logic Track 템플릿

```python
import pytest


def test_d_t1_01_meters_alias_to_meter(g_meters_typo: str) -> None:
    # Given: raw "meters:2.5" (별칭 오타, Mom Test S4)
    # When: normalize_unit("meters") 호출 예정
    # Then: canonical unit "meter" (AC7, F4)
    pytest.fail("RED: D-T1-01 — normalize_unit 미구현, 의도적 실패")
```

## UI Track 템플릿

```python
import pytest


def test_u_t2_01_cli_output_yard_only(g_to_yard: str) -> None:
    # Given: CLI 입력 "meter:2.5:yard" (AC8)
    # When: cli_boundary.run(g_to_yard) 호출 예정
    # Then: 출력에 yard 1줄만, feet/meter 전체 3줄 없음
    pytest.fail("RED: U-T2-01 — cli_boundary 미구현, 의도적 실패")
```

## 절차

1. **설계표 확인** — Test ID, Layer, 파일 경로, 픽스처 이름.
2. **`tests/conftest.py`** — 없으면 생성; 픽스처 `g_meter_2_5`, `g_meters_typo` 등 (reference.md).
3. **`tests/{entity|control|boundary}/test_*.py`** — 테스트 함수 1개(ID 1:1). 클래스 불필요(함수형 pytest).
4. **`src/`·`entity/`·`parser.py` 등 구현 파일 생성·수정 금지.**
5. **pytest 실행** — 단일 노드 `-v`, **FAILED** 확인 (`pytest.fail` 메시지).
6. **RED 보고** — Test ID · FAIL 한 줄 · 변경 파일 `tests/`만.

## pytest 명령 (보고에 포함)

```bash
python -m pytest tests/control/test_d_t1_01.py::test_d_t1_01_meters_alias_to_meter -v
```

ImportError(패키지 미설치) 시: `pip install pytest` 안내. `tests/` 경로 오류는 스켈레톤 수정.

## RED 보고 템플릿

```markdown
## RED Skeleton 보고

- **선언:** Phase: red | Layer: control | Track: Logic
- **Test ID:** D-T1-01
- **pytest:** `python -m pytest …` → FAILED — pytest.fail: RED: D-T1-01 — …
- **변경 파일:** tests/conftest.py, tests/control/test_d_t1_01.py (tests/만)
- **다음:** GREEN — [`/green-minimal`](../green-minimal/SKILL.md)
```

## 완료 문장

`RED 스켈레톤 완료 — pytest FAIL 확인. GREEN은 구현 모듈 추가 후 진행.`

## 금지

| 금지 | |
|------|--|
| `src/`, `entity/`, `control/`, `boundary/` 구현 | |
| assert 기대값 검증 (Then에 fail만) | |
| When에 실제 production import·호출 | GREEN 전 |
| skip / xfail / assert 완화 | |
| Logic Track registry·converter Mock | |
