---
name: golden-master
description: >-
  UnitConverter ARRR Respond Golden Master 구축. /golden-master,
  pytest PASS 후 tests/_approval.py, tests/golden/*.approved.txt,
  UPDATE_GOLDEN=1 baseline, format_contract_output 고정 포맷,
  수동 golden 편집 우회 금지.
disable-model-invocation: true
---

# Golden Master (ARRR — Respond)

`/green-minimal` 등으로 **pytest PASS** 확인 후, 출력·계약을 **golden baseline**으로 고정.

SSOT: [`.cursorrules`](../../../.cursorrules), [reference.md](reference.md), [green-minimal/SKILL.md](../green-minimal/SKILL.md).

## 선행 조건

- 대상 Test ID **PASSED** (assert 기반 GREEN 완료)
- `pytest.fail` RED 스켈레톤 **없음**

## 언제 사용

| 트리거 | 예 |
|--------|-----|
| `/golden-master` | PASS 후 golden 연결·baseline |
| 회귀 방지 | presenter/boundary 출력 문자열 고정 |

**사용하지 않을 때:** RED 설계만, GREEN 미완(PASS 전), golden 파일 **수동 수정**으로 통과, REFACTOR, git commit(사용자 요청 전).

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity|control|boundary | Track: Logic|UI
대상: D-T2-01 (tests/control/test_d_t2_01.py)
```

## 절차

### 0. PASS 재확인

```bash
python -m pytest <대상 노드> -v
```

FAIL이면 `/green-minimal` 먼저.

### 1. `tests/_approval.py`

없으면 생성. 최소:

- `format_contract_output(...)` — [reference.md](reference.md) **고정 키·순서**
- `assert_matches_golden(actual: str, relative: str)` — `UPDATE_GOLDEN=1` 시 baseline 기록, 아니면 diff assert

MagicSquare `int[6]` 계약 **사용 안 함**. UnitConverter는 `input` / `status` / `error` / `lines` / `line_count` 등.

### 2. 테스트에 golden 연결

```python
from _approval import assert_matches_golden, format_contract_output

actual = format_contract_output(
    input_raw=g_to_yard,
    status="OK",
    error="NONE",
    output_lines=[present_line],
)
assert_matches_golden(actual, "d_t2_01_g_to_yard_one_line.approved.txt")
```

- 기존 assert **유지 가능** (golden은 추가 회귀망)
- 이번 턴 **대상 Test ID 하나**만

### 3. baseline 생성

```bash
UPDATE_GOLDEN=1 python -m pytest tests/control/test_d_t2_01.py::test_d_t2_01_yard_one_line -v
```

### 4. 검증 (`UPDATE_GOLDEN` 없음)

```bash
python -m pytest tests/control/test_d_t2_01.py::test_d_t2_01_yard_one_line -v
```

- **matched** — passed, diff 없음
- mismatch — diff 요약 보고, **수동 golden 편집 금지** → 코드·포맷터 수정 또는 `UPDATE_GOLDEN=1` 재실행

### 5. (선택) 파일 스위트

```bash
python -m pytest tests/control/test_d_t2_01.py -v
```

## 규칙

| 규칙 | 내용 |
|------|------|
| 포맷 고정 | reference.md 키·줄 순서; 임의 prose golden 금지 |
| baseline 갱신 | **`UPDATE_GOLDEN=1` pytest만** — 수동 `.approved.txt` 우회 금지 |
| 범위 | 이번 Test ID golden만 |
| Layer | Logic → `format_contract_output` + control/entity 결과 · UI → boundary 캡처 출력 |

## ID 매핑 (사용자 예시)

| 예시 | UnitConverter |
|------|----------------|
| D-SOL-01 | **D-T2-01** (목표 단위 1줄 presenter) |
| U-OUT-01 | **U-T2-01** (CLI 출력) |

## GOLDEN 보고 템플릿

```markdown
## Golden Master 보고

- **대상:** D-T2-01
- **golden:** tests/golden/d_t2_01_g_to_yard_one_line.approved.txt
- **UPDATE_GOLDEN=1:** 생성 완료
- **검증:** matched — pytest passed
- **diff:** 없음 / (요약)
- **변경:** tests/_approval.py, tests/control/test_d_t2_01.py, tests/golden/…
```

완료 한 줄: `Golden Master 완료 — <relative> matched.`

## 금지

| 금지 | |
|------|--|
| PASS 전 golden 생성 | |
| `.approved.txt` 수동 편집으로 통과 | |
| 다른 Test ID 동시 baseline | |
| assert 완화 · skip · xfail | |
| git commit (사용자 요청 전) | |

## ARRR 체인

`/red-test-plan` → `/red-skeleton` → `/green-minimal` → `/golden-master` → [`/refactor-smell`](../refactor-smell/SKILL.md) → `/refactor-safe`(예정)
