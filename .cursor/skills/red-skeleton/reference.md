# RED Skeleton — 파일·픽스처 규칙

선행: `.cursor/skills/red-test-plan/reference.md` (Test ID).

## 디렉터리

```
tests/
  conftest.py          # 공유 픽스처 (로직 데이터만)
  entity/
    test_d_*.py        # Logic · entity
  control/
    test_d_*.py        # Logic · control
  boundary/
    test_u_*.py        # UI · CLI/GUI
```

## 파일명 ↔ Test ID

| Test ID | 파일 | 함수명 패턴 |
|---------|------|-------------|
| D-T1-01 | `tests/control/test_d_t1_01.py` | `test_d_t1_01_*` |
| D-T5-01 | `tests/control/test_d_t5_01.py` | `test_d_t5_01_*` |
| U-T2-01 | `tests/boundary/test_u_t2_01.py` | `test_u_t2_01_*` |

## conftest 픽스처 (예)

```python
import pytest

@pytest.fixture
def g_meter_2_5() -> str:
    return "meter:2.5"

@pytest.fixture
def g_meters_typo() -> str:
    return "meters:2.5"

@pytest.fixture
def g_to_yard() -> str:
    return "meter:2.5:yard"
```

## 상수 import (픽스처 데이터만)

- 목표 SSOT: `entity/constants.py` — `METER_TO_FEET`, `METER_TO_YARD`
- **RED Skeleton 턴:** `entity/constants.py` **생성 금지** (구현=GREEN 이후)
- conftest에서 계수가 필요하면 **픽스처 조립용**으로만 import 시도; 없으면 주석 `# SSOT: entity/constants.py 예정` + fail 테스트는 리터럴 미사용(입력 문자열만)

## UI Track 스켈레톤

- `unittest.mock`으로 `parser`/`converter` 스텁 **허용**
- Then은 여전히 `pytest.fail("RED: U-…")` **한 줄만**
