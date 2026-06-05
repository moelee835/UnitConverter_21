# GREEN Minimal — 모듈·레이어 참조

## 패키지 경로 (UnitConverter_21)

`src/` 없음. 프로젝트 루트:

```
entity/
  constants.py      # METER_TO_FEET, METER_TO_YARD — SSOT
  unit_registry.py  # 단위·별칭·계수 (Phase 0+)
control/
  parser.py         # parse, normalize_unit
  converter.py      # meter 기준 변환
  presenter.py      # 출력 문자열 (I/O 없음)
boundary/
  cli_boundary.py
  gui_boundary.py   # PyQt6 위젯·이벤트 (Tkinter 미사용)
```

## Layer별 최소 구현 허용 범위

| Layer | GREEN 시 추가·수정 | 금지 |
|-------|-------------------|------|
| entity | 상수, registry, 순수 도메인 | `input`/`print`/GUI 프레임워크(`tkinter`, `PyQt6`), boundary/control import |
| control | parser/converter/presenter **대상 함수만** | I/O, boundary 오류 문구 하드코딩 산재(CS) |
| boundary | CLI/GUI 진입·I/O; GUI는 **PyQt6** (`gui_boundary`) | entity 직접 우회, 변환 로직 중복, control에 PyQt6 import |

## Test ID → 구현 위치 (시드)

| Test ID | 최소 구현 위치 |
|---------|----------------|
| D-T1-01 | `control/parser.py` — `normalize_unit` |
| D-T2-01 | `control/presenter.py` — 단일 줄 출력 |
| D-T3-01 | `control/presenter.py` — 3줄 하위 호환 |
| D-T5-01 | import 검사만 (코드 없을 수 있음) |
| U-T2-01 | `boundary/cli_boundary.py` — control 위임 |

## 상수 SSOT

```python
# entity/constants.py
METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361
```

변환 로직은 `entity.unit_registry` 또는 `control/converter.py`에서 constants import — **리터럴 산재 금지** (CS5, CS6).

## UnitConverter vs MagicSquare (오류 코드)

- E001~E007 **없음** — boundary가 사용자 메시지·형식 오류 처리
- entity/control에서 **터미널용 print·input 금지** (AC11, T5)
- Unknown unit·제안은 **control** `parser` / **boundary** 표시 (F6, F7)

## pytest (GREEN 후)

```bash
python -m pytest tests/control/test_d_t1_01.py::test_d_t1_01_meters_alias_to_meter -v
python -m pytest tests/control/test_d_t1_01.py -v
```

## REPL 스모크 (선택)

```python
from control.parser import normalize_unit
assert normalize_unit("meters") == "meter"
```
