# UnitConverter 종합 개선 로드맵

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-06-05 |
| 기준 문서 | [`Code_smell.md`](./Code_smell.md), [`PRD.md`](./PRD.md) §5~§11, [`.cursorrules`](../.cursorrules) |
| 현재 상태 | Sprint A~D **완료**, pytest **31 passed** |
| 미해결 | 없음 (로드맵 v0.2~v1.0 presenter·v0.4 cubit 반영 완료) |

코드 스멜 · 아키텍처 · PRD 세 관점을 하나의 실행 로드맵으로 통합한 문서입니다.

---

## 1. 현재 위치 — 세 관점 교차

| 영역 | 코드 스멜 | 아키텍처 | PRD |
|------|-----------|----------|-----|
| **달성** | 전 항목 해소 | ECB·config SSOT·presenter Strategy | A1~AC12 + v1.0 출력 |
| **잔존** | — | — | — |
| **구조적 강점** | ECB·Feature Envy 해당 없음 | AST 가드, CLI/GUI parity | Mom Test S7·S8 해소 |

**핵심:** v0.2 기능·구조 골격은 완료. 남은 과제는 **SSOT 정리 → 설정·출력 정책 외부화 → 레이어 SRP 강화 → PRD 로드맵(v0.3~v1.0) 순 진화**.

---

## 2. 통합 개선 매트릭스

| # | 이슈 | CS | 아키텍처 | PRD / Mom Test | 통합 조치 | PRD 버전 | 턴 유형 |
|---|------|-----|----------|----------------|-----------|----------|---------|
| 1 | GUI `UNIT_OPTIONS` ≠ registry | CS3, CS6 | SSOT 위반, OCP 재발 위험 | G1 단위 목록은 registry와 일치 | `gui_boundary` → `registry.names()` + DI(선택) | v0.2 잔여 | `/refactor-safe` |
| 2 | 계수·단위 Python 내장 | CS5 | infra 계층 미사용 | §11 v0.4 설정 외부화; README 실습 | `config/units.json` → `config_loader` → `UnitRegistry.from_config()` | v0.4 (선행 가능) | `/refactor-safe` |
| 3 | Raw float 출력 | CS13 | presenter 정책 부재 | AC10, S9 신뢰 | `format_number()` + `DISPLAY_PRECISION` | v0.2 AC10 | `/refactor-safe` + golden |
| 4 | 별칭 `_UNIT_ALIASES` 분리 | CS10, S4 | parser↔registry SSOT 불일치 | F4, AC7, S4 | alias → config/registry `resolve_alias()` | v0.2~v0.4 | refactor → v0.3 VO |
| 5 | 오류 메시지 in parser | CS12 | presenter SRP 위반 | F6, F7, S6 | `error_presenter` → `output_formatter` 이동 | v0.3 SRP | `/refactor-safe` |
| 6 | `conversion_flow` T5 미검사 | AC11 | 정적 검사 hole | Phase 6 AC11 강화 | `g_app_module_names`에 `conversion_flow` 추가 | v0.3 | 테스트만 |
| 7 | domain `ValueError` 문자열 | — | 계층 경계 모호 | A1 domain UX 금지 | `UnknownUnitError` 타입, 메시지는 app | v0.3 | refactor |
| 8 | `default_registry()` 전역 | CS5 | composition root 없음 | v0.4 config path 주입 | boundary에서 registry 생성·주입 | v0.4 | refactor |
| 9 | GUI `__init__` 장문 | CS1 | boundary 가독성 | G3 확장 전 정리 | `_build_ui()` Extract Method | P2 | `/refactor-safe` |
| 10 | 음수 미검증 | CS8 | parse 검증 부재 | README 갭 | Guard Clause in `parse_input` | 신규 AC | **GREEN** |
| 11 | G3 인라인 오류 UX | — | GUI error_label만 | G3 P1 | 오류 시 제안·목록 UI 강화 | v0.2 P1 | GREEN |
| 12 | json/csv 출력 | — | presenter 단일 포맷 | v1.0 | Presenter Strategy 패턴 | v1.0 | feature |

---

## 3. 버전별 통합 로드맵

### Sprint A — v0.2 잔여 마무리

| 순서 | 조치 | 상태 |
|------|------|------|
| A1 | GUI `UNIT_OPTIONS` → `registry.names()` | ✅ |
| A2 | `format_line` 반올림 정책 | ✅ |
| A3 | G3 GUI 오류 UX | ✅ (U-GUI-04 PASS) |

### Sprint B — v0.3 OCP · SRP · AC11

| 순서 | 조치 | 상태 |
|------|------|------|
| B1 | `format_unknown_unit_message` → presenter | ✅ |
| B2 | T5에 `conversion_flow` 포함 | ✅ |
| B3 | `UnitRegistry.resolve_alias()` API | ✅ (C3와 통합) |
| B4 | `UnitId` value object | ✅ (type alias) |
| B5 | `UnknownUnitError` (domain) | ✅ |

### Sprint C — v0.4 설정 외부화

| 순서 | 조치 | 상태 |
|------|------|------|
| C1 | `config/units.json` + `load_config` | ✅ |
| C2 | `UnitRegistry.from_config()` | ✅ |
| C3 | aliases + suggest_cutoff in config | ✅ |
| C4 | boundary composition root | ✅ |

### 기타

| 조치 | 상태 |
|------|------|
| CS1 `_build_ui()` Extract Method | ✅ |
| CS8 음수 검증 (GREEN) | ✅ `test_d_t4_03` |
| CLI prompt 상수 (`CLI_PROMPT`) | ✅ |

**설정 로드 체인 (ECB 고정):**

```
config/units.json
  → infrastructure/config_loader.load_config()
  → domain/unit_registry.UnitRegistry.from_config()
  → app/conversion_flow(registry=...)
  → boundary/cli · gui_boundary (registry 주입)
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

### Sprint D — v1.0 presenter · v0.4 cubit

| 순서 | 조치 | 상태 |
|------|------|------|
| D1 | json \| csv \| table Presenter Strategy | ✅ `format_result_lines`, `meter:2.5:yard:json` |
| D2 | cubit `units.json` config 등록 | ✅ |
| D3 | `UnitRegistry.register()` 런타임 API | ✅ |
| D4 | golden·테스트 갱신 (cubit 4단위) | ✅ |

### 적용 순서 (기법 체인)

앞 항목이 뒤 항목의 전제.

```
A1 CS6 (GUI→registry SSOT)
  → A2 CS13 (AC10 출력 정책)
  → B1~B5 (v0.3 SRP·OCP·AC11)
  → C1~C4 (v0.4 config)
  → D (v1.0 presenter)
```

CS8(음수), G3(UX)은 refactor-safe가 **아님** — 별도 GREEN 턴.

---

## 4. Mom Test · AC 관점 종합

| Evidence / AC | 현재 | 통합 개선 | Sprint |
|---------------|------|-----------|--------|
| S4 (`meters` 오타) | 별칭 1개 | config alias + `resolve_alias()` | B3 → C3 |
| S6 (5분 재작업) | F6/F7 부분 | presenter 분리 + G3 UX | B1, A3 |
| S7·S8 (3줄 불필요) | 해소 | `to_unit` 생략 시 3줄 하위 호환 유지 | — |
| S9 (float 신뢰) | raw float | AC10 `format_number` | A2 |
| AC10 | 미완 | CS13 = PRD AC10 직결 | A2 |
| AC11 | 부분 (T5 hole) | app 전 모듈 AST | B2 |
| AC12 | T6 PASS | CS6 후에도 `convert_parsed` 경로 유지 | A1 |

---

## 5. 아키텍처 불변 원칙

개선 작업 전후 **반드시 유지**할 구조적 불변식.

| 원칙 | 내용 | 깨지면 |
|------|------|--------|
| Single Conversion Path | CLI·GUI → `parse_input` → `convert_parsed` | AC12 붕괴 |
| ECB 의존 | boundary → app → domain | AC11, T5 실패 |
| Meter hub | feet↔yard 직접 API 없음 | PRD §2.3 비목표 위반 |
| Presenter 단일화 | 출력 문자열은 `output_formatter` | CS13·CS12 재발 |
| Registry SSOT | 단위·계수·(향후) alias의 단일 출처 | CS3·CS6 재발 |
| Golden 계약 | 리팩터는 구조만; 포맷 변경은 문서+golden | 회귀 은폐 |

---

## 6. 턴 유형 구분

| 유형 | 대상 | pytest | golden | 예 |
|------|------|--------|--------|-----|
| `/refactor-safe` | 구조·SSOT, **동작 불변** | PASS 필수 | 대부분 유지 | CS6, CS5(값 동일), CS12 이동 |
| `/refactor-safe` + golden | 출력 **정책** 명시 | PASS | 의도적 갱신 | CS13 / AC10 |
| GREEN | **행동·AC 추가** | Red→Green | 새 golden | CS8 음수, G3 |

---

## 7. 우선 실행 권고

| 우선순위 | 조치 | 이유 (세 관점 동시) |
|----------|------|---------------------|
| **1순위** | CS6 — GUI → `registry.names()` | 스멜(DRY) + 아키텍처(SSOT) + PRD(G1); 1파일, golden 무영향 |
| **2순위** | CS13 — AC10 출력 정책 | Mom Test S9 + PRD AC10; presenter 정책 확립 |
| **3순위** | CS5 — `units.json` (v0.4 선행) | README·PRD + infra 슬롯; CS6 이후가 자연스러움 |
| **4순위** | v0.3 묶음 (B1~B5) | SRP·AC11·OCP — Phase 6 |
| **별도** | CS8, G3 | PRD P1/GREEN — refactor와 분리 |

---

## 8. Code_smell P vs PRD 버전 정렬

| Code_smell P | PRD 공식 버전 | 통합 판단 |
|--------------|---------------|-----------|
| P0 CS6 | v0.2 잔여 | **즉시** — PRD G1과 직결 |
| P0 CS13 | v0.2 AC10 | **즉시** — Mom Test S9 |
| P0 CS5 | v0.4 | Sprint C — CS6 후; README는 앞당겨도 됨 |
| P1 CS10, CS12 | v0.2 P1 ~ v0.3 | Sprint B |
| P2 CS1, CS8 | P2 / README | 여유 또는 GREEN |

---

## 9. Change Budget (`/refactor-safe` 공통)

| 항목 | 한도 |
|------|------|
| 파일 | ≤ 3 |
| 클래스 | ≤ 1 |
| 메서드 | ≤ 3 |

Budget 초과 시 이번 턴 중단 — 분할안만 제안. 상세 스멜·기법 매핑은 [`Code_smell.md`](./Code_smell.md) 참조.

---

## 10. 완료

로드맵 Sprint A~D 전부 적용 완료. 신규 기능 추가 시 [`PRD.md`](./PRD.md) §11 이후 항목 참조.

- 보고서: [`Reports/09_UnitConverter_Refactor-Improvement_Report.md`](../Reports/09_UnitConverter_Refactor-Improvement_Report.md)
- Transcript: [`Prompts/08_UnitConverter_Refactor-Improvement-Transcript.md`](../Prompts/08_UnitConverter_Refactor-Improvement-Transcript.md)
