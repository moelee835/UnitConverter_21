# Refactor Safe — 예시 매핑 · 검증

## MagicSquare → UnitConverter (호출 예시)

| 원본 | UnitConverter |
|------|----------------|
| Duplicated 10선 합 4곳 | **CS5·CS6** — `to_meter` if-elif + `* 3.28084` / `* 1.09361` + print 3줄 |
| `src/entity/validation.py` | `UnitConverter.py:main` 또는 `control/converter.py` |
| `sum_row`, `sum_col` extract | `to_meter(value, unit)`, `from_meter(meter_value, unit)` |
| int[6] 1-index 금지 | **출력 문자열 O3** · 파싱 `unit:value[:to]` **동일** |
| entity E001~E005 | entity에 **print/input/사용자 오류 메시지** 금지 |

## Budget 예 (CS6)

| 항목 | 값 |
|------|-----|
| 파일 | `entity/constants.py`, `control/converter.py` (2) |
| 메서드 | `to_meter`, `from_meter` (2 extract) |
| 클래스 | 0 |

`UnitConverter.py`는 boundary 위임만 남기면 **파일 3** — Budget 초과 시 converter만 먼저.

## 검증 명령

```bash
# 1) 회귀
python -m pytest tests/ -v

# 2) golden (대상 테스트·파일 지정)
python -m pytest tests/control/test_d_t2_01.py -v
# UPDATE_GOLDEN 없이 — matched 기대
```

`tests/`·`tests/golden/` 없으면: full pytest + **수동 AC 스모크** (`meter:2.5` 3줄 동일) 보고.

## Golden diff 정책

| diff | 조치 |
|------|------|
| **비의도** (포맷·순서·오타) | **롤백** 리팩터 |
| **의도** (반올림 정책 명시·공백 LF 통일) | `docs/` 또는 `Reports/` 근거 1줄 + `UPDATE_GOLDEN=1` 재실행 |

## 선행

- `/refactor-smell` → `docs/Code_smell.md` 에서 **P0 1개** 선택
- pytest **전체 PASS**

## 금지 (리팩터 턴)

- F4~F7·GUI 신규 동작 (별도 GREEN)
- assert 완화 · skip · xfail
- Mom Test AC7/8 **행동 변경** (구조만 이동)
