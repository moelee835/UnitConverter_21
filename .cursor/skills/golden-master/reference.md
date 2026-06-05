# Golden Master — 포맷 · 경로 (UnitConverter)

## 디렉터리

```
tests/
  _approval.py              # assert_matches_golden, format_contract_output
  golden/
    *.approved.txt          # baseline (UTF-8, LF, trailing newline)
```

## Golden 파일명 (시드)

| Test ID | relative path |
|---------|----------------|
| D-T1-01 | `d_t1_01_meters_alias.approved.txt` |
| D-T2-01 | `d_t2_01_g_to_yard_one_line.approved.txt` |
| D-T3-01 | `d_t3_01_meter_2_5_three_lines.approved.txt` |
| D-T4-01 | `d_t4_01_unknown_abc.approved.txt` |
| U-T2-01 | `u_t2_01_cli_yard_only.approved.txt` |
| U-T4-01 | `u_t4_01_unknown_with_suggestion.approved.txt` |

## `format_contract_output` 고정 필드 (UTF-8, LF)

순서 고정 · 알 수 없는 키 추가 금지(버전 bump 시 문서화).

| 키 | 설명 |
|----|------|
| `input:` | raw CLI/GUI 입력 문자열 (trim 정책 반영 후 또는 전) |
| `status:` | `OK` \| `ERROR` |
| `error:` | 성공 `NONE` · 실패 `UNKNOWN_UNIT` \| `INVALID_FORMAT` \| `INVALID_NUMBER` 등 |
| `lines:` | 다음 줄부터 출력 줄 (O3: `{v} {from} = {conv} {to}`) |
| `line_count:` | 출력 줄 수 (AC8: 1 / AC1: 3) |
| `canonical_from:` | (선택) 정규화된 from unit |
| `canonical_to:` | (선택) 목표 unit |
| `hint:` | (선택) `Did you mean meter?` — F6 |

**예 (성공 · yard 1줄, AC8):**

```text
input: meter:2.5:yard
status: OK
error: NONE
lines:
2.5 meter = 2.734025 yard
line_count: 1
```

**예 (오류 · Unknown):**

```text
input: abc:1
status: ERROR
error: UNKNOWN_UNIT
lines:
Unknown unit: abc
line_count: 1
hint: Did you mean meter?
```

- **소수:** AC10 정책에 맞춘 **고정 문자열** (golden 생성 시 반올림 규칙 명시)
- **int[6]·격자 없음** — MagicSquare 계약 미사용

## `assert_matches_golden(actual, relative)`

- `relative` → `tests/golden/{relative}`
- `UPDATE_GOLDEN=1` → baseline **덮어쓰기** (수동 `.approved.txt` 편집으로 통과 **금지**)

## pytest

```bash
# baseline 생성
UPDATE_GOLDEN=1 python -m pytest tests/control/test_d_t2_01.py::test_d_t2_01_yard_one_line -v

# 검증
python -m pytest tests/control/test_d_t2_01.py::test_d_t2_01_yard_one_line -v
```

## Test ID 매핑 (D-SOL-01 / U-OUT-01)

| 원본 예시 ID | UnitConverter |
|--------------|----------------|
| D-SOL-01 | **D-T2-01** — presenter 단일 줄 (G_to_yard) |
| U-OUT-01 | **U-T2-01** — boundary CLI 캡처 출력 |
