# Code Smell Report — UnitConverter

| 스캔 일시 | 2026-06-05 |
|-----------|------------|
| pytest | `tests/` 전체 **23 passed** (0.21s) |
| 스캔 범위 | `UnitConverter.py`, `unit_converter/domain\|app\|cli\|gui_boundary\|infrastructure`, `tests/` |
| JSON/YAML | 프로젝트 내 `.json`/`.yaml` **0건** — 단위·계수는 Python 하드코딩 |
| SSOT | [`PRD.md`](./PRD.md) §9, [`.cursorrules`](../.cursorrules), Mom Test S1~S9 |
| 종합 로드맵 | [`Improvement_Roadmap.md`](./Improvement_Roadmap.md) — 스멜·아키텍처·PRD 통합 개선안 |

---

## 리팩터링 기법 매핑 (미해결 스멜)

Fowler 리팩터링 카탈로그 + ECB·SSOT 관점. **1차 기법** = 이번 턴 `/refactor-safe`에 적용할 핵심.

| 우선순위 | CS | 스멜 | 위치 | **1차 기법** | **2차·보조 기법** | 적용 결과 | Budget |
|----------|-----|------|------|-------------|------------------|-----------|--------|
| **P0** | CS3, CS6 | 단위 목록 이중 정의 | `gui_boundary` ↔ `unit_registry` | **Remove Duplication** (DRY) | **Move Method** — registry가 SSOT, GUI는 조회만 | `UNIT_OPTIONS` 삭제 → `default_registry().names()` | 1파일·1메서드 |
| **P0** | CS5 | Magic Number / 설정 미외부화 | `unit_registry.py` | **Replace Magic Number with Named Constant** | **Externalize Configuration** — JSON/YAML + `config_loader` | 계수·단위 정의가 코드 밖으로 | 3파일 |
| **P0** | CS13, S9 | Raw float 출력 | `output_formatter.format_line` | **Extract Function** — `format_number(value, precision)` | **Introduce Explaining Variable** — `DISPLAY_PRECISION = 6` | 출력 정책 한곳 집중 | 1파일·1함수 |
| **P1** | CS10, S4 | Primitive Obsession (별칭) | `input_parser._UNIT_ALIASES` | **Replace Data Value with Object** | **Move Field** — alias를 parser → registry/config | 별칭 확장 시 코드 수정 불필요 | 2파일 |
| **P1** | CS5 | Magic Number `0.6` | `input_parser.suggest_unit` | **Replace Magic Number with Named Constant** | **Externalize Configuration** — `suggest_cutoff` in JSON | 의미·튜닝 가능 | 1파일 |
| **P1** | CS12 | Hard-coded 메시지 | `format_unknown_unit_message` | **Extract Constant** — 템플릿 상수 | **Move Method** — presenter(`output_formatter`)로 이동 | domain/app 역할 분리 | 1~2파일 |
| **P1** | CS12 | Hard-coded CLI prompt | `cli.run_session` | **Extract Constant** | **Parameterize Method** — `run_session(prompt=...)` | boundary 상수화 | 1파일 |
| **P2** | CS1 | Long Method | `UnitConverterWindow.__init__` | **Extract Method** — `_build_ui()` | **Extract Class** — Budget 초과 시 2턴 분할 | UI 조립 분리 | 1파일·1메서드 |
| **P2** | CS8 | 음수 미검증 | `parse_input` | **Guard Clause** | **Extract Function** — `validate_value(value)` | parse 단계 검증 | 1파일·1함수 |
| — | CS4, AC11 | ECB 위반 | — | — | T5·`test_d_arc_01` PASS | **해당 없음** | — |
| — | CS4, CS10 | Feature Envy | — | — | CLI/GUI → `convert_parsed` 경유 | **해당 없음** | — |

---

## 기법별 상세

### P0 CS6 — 단위 목록 이중 (Duplicated Code)

| 기법 | 적용 |
|------|------|
| Remove Duplication | GUI와 registry에 동일 `["meter","feet","yard"]` 2벌 → 1벌만 유지 |
| Move Method | “지원 단위 목록” 책임을 `UnitRegistry.names()`로 이동 |
| Dependency Injection (경량) | `UnitConverterWindow(registry=default_registry())` — 테스트·확장 용이 |

```python
# Before — unit_converter/gui_boundary.py
UNIT_OPTIONS = ["meter", "feet", "yard"]

# After
from unit_converter.domain.unit_registry import default_registry
options = default_registry().names()
self.from_unit.addItems(options)
```

**금지:** GUI에 변환 로직 추가 (Feature Envy 유발).

---

### P0 CS5 — Magic Number / 설정 미외부화

| 기법 | 적용 |
|------|------|
| Replace Magic Number with Named Constant | `3.28084` → `FEET_PER_METER` (부분 적용됨) |
| Externalize Configuration | 상수를 `config/units.json`으로 이동 |
| Introduce Factory Method | `UnitRegistry.from_config(path)` — JSON → `_BuiltinUnit` 생성 |
| Replace Conditional with Polymorphism (v0.3) | if-elif 대신 registry lookup (v0.2 골격 완료) |

**로드 체인 (ECB 준수):**

```
config/units.json
  → infrastructure/config_loader.load_config()
  → domain/unit_registry.UnitRegistry.from_config()
  → app / gui_boundary는 registry만 참조
```

**현재 코드:**

```python
# unit_converter/domain/unit_registry.py
FEET_PER_METER = 3.28084
YARD_PER_METER = 1.09361
_BUILTIN = {
    "meter": _BuiltinUnit("meter", 1.0, 1.0),
    "feet":  _BuiltinUnit("feet",  FEET_PER_METER, FEET_PER_METER),
    "yard":  _BuiltinUnit("yard",  YARD_PER_METER, YARD_PER_METER),
}

# unit_converter/infrastructure/config_loader.py — 스텁
def load_config(_path: str) -> dict:
    raise NotImplementedError("config_loader is planned for v0.4 (PRD §11)")
```

**제안 스키마 (`config/units.json`):**

```json
{
  "units": [
    { "id": "meter", "to_meter_factor": 1.0,     "from_meter_factor": 1.0 },
    { "id": "feet",  "to_meter_factor": 3.28084,  "from_meter_factor": 3.28084 },
    { "id": "yard",  "to_meter_factor": 1.09361,  "from_meter_factor": 1.09361 }
  ],
  "aliases": { "meters": "meter" },
  "suggest_cutoff": 0.6
}
```

---

### P0 CS13 — Raw float 출력

| 기법 | 적용 |
|------|------|
| Extract Function | `format_line` 내부 숫자 포맷 → `_format_value(x: float) -> str` |
| Replace Magic Number with Named Constant | `OUTPUT_DECIMALS = 6` |
| Single Point of Formatting | CLI·GUI 모두 `output_formatter` 경유 (구조상 이미 만족) |

**주의:** golden(`2.734025`)과 불일치 시 **의도적 golden 갱신** — `docs/` 근거 1줄 + `UPDATE_GOLDEN=1`.

---

### P1 CS10 — 별칭 Primitive Obsession

| 기법 | 적용 |
|------|------|
| Replace Primitive with Object | `str` → `UnitId` value object (v0.3+) |
| Move Field | `_UNIT_ALIASES`를 `input_parser` → `UnitRegistry` 또는 config |
| Encapsulate Collection | alias dict 직접 노출 금지 → `registry.resolve_alias(raw)` API |

**단계적 접근:** (1) config `aliases` 추가 → (2) `normalize_unit()`이 registry/config 조회 → (3) v0.3 `UnitId` 도입.

---

### P1 CS12 · CS5(cutoff) · P2 CS1 · CS8

| CS | 1차 기법 | 비고 |
|----|----------|------|
| CS12 메시지 | Extract Constant + Move Method → `output_formatter` | entity에 사용자 메시지 **추가 금지** |
| CS12 CLI prompt | Extract Constant | boundary 전용 |
| CS5 cutoff `0.6` | Replace Magic Number with Named Constant | CS5 JSON 외부화 시 함께 이동 |
| CS1 Long `__init__` | Extract Method `_build_ui()` | Extract Class는 Budget 2턴 |
| CS8 음수 | Guard Clause | **행동 변경** → `/refactor-safe` 아닌 별도 GREEN 턴 |

---

## 이미 해소된 스멜 → 적용 기법

| CS | 스멜 | 적용 기법 | 결과 위치 |
|----|------|-----------|-----------|
| CS3 | OCP if-elif | Replace Conditional with Polymorphism + Introduce Registry | `unit_registry.py`, `converter.py` |
| CS4 | I/O in main | Extract Class (boundary) + Move Method | `cli.py`, `gui_boundary.py` |
| CS6 | 변환 이중 | Extract Method + Remove Duplication | `converter.py` |
| CS9 | No trim | Normalize Input (`strip().lower()`) | `input_parser.normalize_unit` |
| CS14 | Hard-coded 3줄 | Extract Method | `format_single_line` / `format_all_lines` |
| CS4, AC11 | ECB | Layered Architecture (boundary→app→domain) | 전체 패키지 |

---

## Mom Test · PRD 연결

| Evidence | CS | 현재 상태 | 대응 기법 |
|----------|-----|-----------|-----------|
| S4 (`meters` 오타) | CS10 | 별칭 1개만 | Move Field + Externalize Configuration |
| S7·S8 (불필요 3줄) | CS14 | **해소** | Extract Method |
| S9 (float 신뢰) | CS13 | **미해소** | Extract Function + Named Constant |
| S3 (trim) | CS9 | **해소** | Normalize Input |
| S6 (5분 재작업) | CS10, F6/F7 | 부분 해소 | Move Field (alias), Extract Constant (메시지) |

---

## 리팩터링 적용 순서 (기법 체인)

앞 항목이 뒤 항목의 전제.

| 순서 | CS | 핵심 기법 | 이유 |
|------|-----|-----------|------|
| 1 | CS6 | Remove Duplication | registry SSOT 확립 — config·GUI 모두 registry 참조 |
| 2 | CS5 | Externalize Configuration | SSOT가 코드 → JSON |
| 3 | CS10 | Move Field + Externalize | alias가 config와 같은 파일에 합류 |
| 4 | CS13 | Extract Function | 출력 정책 단일화 (golden 영향 격리) |
| 5 | CS12, cutoff | Extract Constant | literal 정리 |
| 6 | CS1 | Extract Method | UI 구조만 정리, 동작 불변 |
| — | CS8 | Guard Clause | **별도 GREEN 턴** (계약 변경) |

---

## Change Budget (`/refactor-safe` 공통)

| 항목 | 한도 |
|------|------|
| 파일 | ≤ 3 |
| 클래스 | ≤ 1 |
| 메서드 | ≤ 3 |

Budget 초과 시 **이번 턴 중단** — 분할안만 제안.

---

## `/refactor-safe` 후보 (Budget 내)

| # | CS | 핵심 기법 | 대상 | pytest | golden |
|---|-----|-----------|------|--------|--------|
| 1 | CS6 | Remove Duplication, Move Method | `gui_boundary.py` — `UNIT_OPTIONS` → `registry.names()` | PASS 유지 | 영향 없음 |
| 2 | CS5 | Externalize Configuration, Factory Method | `config/units.json` + `config_loader` + `UnitRegistry.from_config` | PASS 유지 | 값 동일 시 영향 없음 |
| 3 | CS13 | Extract Function, Named Constant | `output_formatter.format_line` 반올림 | PASS 유지 | **갱신 필요** |

**권장:** P0 **CS6** 1개부터 (리스크 최소). CS5(JSON/YAML)는 다음 스프린트.

---

## 기법 사용 금지·주의

| 상황 | 피할 기법 | 이유 |
|------|-----------|------|
| entity에 오류 메시지 | Move Method → domain | AC11, refactor-safe 금지 |
| 단위 추가마다 if-elif | Conditional 추가 | CS3 재발 |
| Budget 초과 한 턴 | Extract Class + Externalize + Format 동시 | 파일 > 3 |
| CS8 음수 검증 | refactor-safe에 Guard Clause | **행동 변경** → GREEN 턴 |

---

## 다음 단계

**가장 P0 1개(CS6)만 골라 `/refactor-safe` 실행하세요.**

```
Phase: refactor | Scope: gui_boundary.py | Track: Logic+UI
스멜: Duplicated unit list (CS6) | Budget: 파일≤1 · 메서드≤1
```
