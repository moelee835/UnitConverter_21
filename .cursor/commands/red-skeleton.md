# /red-skeleton — RED 테스트 골격 작성

UnitConverter Dual Track — `/red-test-plan` **설계표 확정 후** `tests/` 스켈레톤만 작성.  
`.cursorrules`, `.cursor/skills/red-skeleton/SKILL.md`, `.cursor/skills/red-test-plan/` 와 함께 적용.

**허용 diff:** `tests/**`, `tests/conftest.py` **만**.  
**금지:** `src/`, `entity/`, `control/`, `boundary/`, `UnitConverter.py` 구현 로직 추가·리팩터(GREEN).

---

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: entity|control|boundary | Track: Logic|UI
Test ID: <D-* 또는 U-*>
```

사용자가 설계표·파일 경로를 주면 그대로 따른다. 없으면 직전 `/red-test-plan` 출력을 요청한다.

---

## 스켈레톤 규칙

| 항목 | 규칙 |
|------|------|
| AAA | `# Given:` / `# When:` / `# Then:` 주석 |
| Then | `pytest.fail("RED: <Test ID> — …")` **한 줄만** |
| assert | 본문·통과 더미·skip·xfail **금지** |
| When | **주석만** — 구현 함수 호출·import는 GREEN까지 보류 |
| Given | `tests/conftest.py` 픽스처 (로직 데이터, Mock 아님) |
| 상수 | `entity/constants.py` — **픽스처 조립 시만** import; 없으면 문자열 픽스처만 (Skeleton에서 constants.py **생성 금지**) |
| Track | Logic → Domain Mock 금지 / UI → control Mock 허용(When 주석·setup만, Then은 fail 한 줄) |

---

## 절차

1. 설계표에서 **Test ID · 파일 · 픽스처** 확인.
2. `tests/conftest.py` — `g_meter_2_5`, `g_meters_typo`, `g_to_yard` 등 (reference.md).
3. `tests/{entity|control|boundary}/test_<id>.py` — 함수 1개 : Test ID 1:1.
4. **pytest 실행** — 아래 형식, **FAILED** 확인.
5. **RED 보고** — Test ID · FAIL 한 줄 · 변경 파일(tests/만).

---

## 코드 템플릿 (Logic · control 예: D-T1-01)

```python
import pytest


def test_d_t1_01_meters_alias_to_meter(g_meters_typo: str) -> None:
    # Given: raw "meters:2.5" (G_meters_typo, Mom Test S4)
    # When: normalize_unit("meters") 호출 예정
    # Then: canonical "meter" (PRD F4, AC7, T1)
    pytest.fail("RED: D-T1-01 — normalize_unit 미구현, 의도적 실패")
```

---

## 호출 예시 (사용자 메시지)

```
/red-skeleton
Phase: red | Layer: control | Track: Logic
앞에서 확정한 설계표 기준으로 RED 스켈레톤만 작성해.
Test ID: D-T1-01
파일: tests/control/test_d_t1_01.py
픽스처: tests/conftest.py (g_meters_typo — "meters:2.5")
규칙:
- AAA 주석 (Given / When / Then)
- Then은 pytest.fail("RED: D-T1-01 — …") 한 줄만
- assert 본문·skip·xfail·통과 더미 금지
- src/·entity/·control/ 구현 모듈 수정 금지
완료 후 실행하고 보고:
python -m pytest tests/control/test_d_t1_01.py::test_d_t1_01_meters_alias_to_meter -v
보고: Test ID · FAIL 한 줄 · 변경 파일(tests/만)
```

---

## pytest 예시 (bash)

```bash
# 프로젝트 루트
python -m pytest tests/control/test_d_t1_01.py::test_d_t1_01_meters_alias_to_meter -v

# entity layer
python -m pytest tests/entity/test_d_t5_01.py -v

# boundary (UI)
python -m pytest tests/boundary/test_u_t2_01.py -v
```

**기대:** `FAILED` + 메시지 `RED: <Test ID>`. `PASSED`면 스켈레톤 규칙 위반.

---

## RED 보고 형식

```markdown
## RED Skeleton 보고

- **Test ID:** D-T1-01
- **pytest:** FAILED — pytest.fail: RED: D-T1-01 — …
- **변경 파일:** tests/conftest.py, tests/control/test_d_t1_01.py
- **다음:** GREEN (구현 모듈 + assert 전환)
```

완료 한 줄: `RED 스켈레톤 완료 — pytest FAIL 확인. GREEN은 구현 후 진행.`

---

## 금지

| 금지 | |
|------|--|
| 구현 모듈(`parser.py`, `entity/`, …) 생성·수정 | |
| Then에 assert 기대값 | |
| skip / xfail / `assert True` | |
| GREEN / REFACTOR 동시 진행 | |
| Logic Track registry·converter Mock | |

---

## 이전 · 다음 Command

| Command | 역할 |
|---------|------|
| `/red-test-plan` | 설계표·C2C (파일 없음) |
| `/red-skeleton` | **본 Command** — tests 골격 |
| [`/green-minimal`](../commands/green-minimal.md) | 최소 구현 GREEN |
