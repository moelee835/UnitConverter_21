# /golden-master — ARRR Respond · Golden Master

UnitConverter — **pytest PASS 확인 후** 출력·계약 baseline 고정.  
`.cursorrules`, `.cursor/skills/golden-master/SKILL.md`, [reference.md](../skills/golden-master/reference.md).

**git commit:** 사용자 요청 시만.

---

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity|control|boundary | Track: Logic|UI
대상: <Test ID> (<tests/.../test_*.py>)
```

---

## 선행 조건

- `/green-minimal` 등으로 해당 테스트 **PASSED**
- RED `pytest.fail` 제거 완료

---

## 절차

### 1. PASS 확인

```bash
python -m pytest <tests/.../test_*.py>::<test_function> -v
```

### 2. `tests/_approval.py` (없으면 생성)

- `format_contract_output(...)` — UnitConverter **고정 텍스트 계약** ([reference.md](../skills/golden-master/reference.md))
- `assert_matches_golden(actual, relative)` — `tests/golden/{relative}` 비교

`UPDATE_GOLDEN=1` → baseline **기록** (수동 파일 편집으로 통과 우회 **금지**).

### 3. 테스트에 golden 경로 연결

```python
assert_matches_golden(actual, "d_t2_01_g_to_yard_one_line.approved.txt")
```

### 4. baseline 생성 (bash)

```bash
UPDATE_GOLDEN=1 python -m pytest tests/control/test_d_t2_01.py::test_d_t2_01_yard_one_line -v
```

### 5. 검증 (`UPDATE_GOLDEN` 없음 → matched)

```bash
python -m pytest tests/control/test_d_t2_01.py::test_d_t2_01_yard_one_line -v
python -m pytest tests/control/test_d_t2_01.py -v
```

---

## 호출 예시 (사용자 메시지)

```
/golden-master
Phase: green | Layer: control | Track: Logic
대상: D-T2-01 (또는 boundary U-T2-01)
pytest PASS 상태 확인 후 Golden Master만 구축해.
1. tests/_approval.py — assert_matches_golden(actual, relative) (없으면 생성)
2. 테스트에 golden 경로 연결:
   tests/golden/d_t2_01_g_to_yard_one_line.approved.txt
3. 기준 파일 생성 (bash):
   UPDATE_GOLDEN=1 python -m pytest tests/control/test_d_t2_01.py::test_d_t2_01_yard_one_line -v
4. 검증 (UPDATE_GOLDEN 없음) → matched 확인:
   python -m pytest tests/control/test_d_t2_01.py::test_d_t2_01_yard_one_line -v
규칙:
- UnitConverter 고정 포맷 (input/status/error/lines/line_count) — reference.md
- golden 수동 편집으로 통과 우회 금지
보고: golden 파일 경로 · matched 여부 · diff 있으면 내용 요약
git commit은 내가 요청할 때만.
```

---

## UnitConverter vs MagicSquare

| MagicSquare | UnitConverter |
|-------------|----------------|
| `int[6]` 1-index | **없음** — `lines:` + `line_count:` |
| `error: E003 …` | `error: UNKNOWN_UNIT` 등 PRD 동작 문자열 |
| `D-SOL-01` | **D-T2-01** (yard 1줄) |
| `U-OUT-01` | **U-T2-01** (CLI 출력) |

---

## `format_contract_output` 요약

고정 줄 순서 (상세는 reference.md):

```text
input: <raw>
status: OK|ERROR
error: NONE|UNKNOWN_UNIT|...
lines:
<line1>
<line2>
line_count: N
```

성공 예 (`meter:2.5:yard`, AC8):

```text
input: meter:2.5:yard
status: OK
error: NONE
lines:
2.5 meter = 2.734025 yard
line_count: 1
```

---

## GOLDEN 보고 형식

```markdown
## Golden Master 보고

- **대상 Test ID:** D-T2-01
- **golden 경로:** tests/golden/d_t2_01_g_to_yard_one_line.approved.txt
- **matched:** 예 / 아니오
- **diff:** (있으면 unified diff 요약)
- **변경 파일:** tests/_approval.py, tests/.../test_*.py, tests/golden/...
```

완료 한 줄: `Golden Master 완료 — matched.`

---

## 금지

| 금지 | |
|------|--|
| PASS 전 golden | |
| `.approved.txt` 수동 수정으로 통과 | |
| 이번 Test ID 외 golden 일괄 | |
| RED / GREEN 재구현 (golden만) | |
| assert 완화 · skip · xfail | |
| git commit (명시 요청 전) | |

---

## ARRR Command 체인

| # | Command |
|---|---------|
| 1 | `/red-test-plan` |
| 2 | `/red-skeleton` |
| 3 | `/green-minimal` |
| 4 | **`/golden-master`** |
| 5 | [`/refactor-smell`](../commands/refactor-smell.md) |
| 6 | `/refactor-safe` (예정) |
