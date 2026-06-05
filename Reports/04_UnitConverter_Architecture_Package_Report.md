# 04. UnitConverter 패키지 아키텍처·RED 설계 보고서

| 항목 | 내용 |
|------|------|
| 제품 | UnitConverter — 길이 단위 변환 (CLI + GUI) |
| 작성일 | 2026-06-05 |
| 상태 | Complete — PRD·cursorrules·패키지·RED 스켈레톤·README 반영 |
| 연계 | [`docs/PRD.md`](../docs/PRD.md) §5.6, [`.cursorrules`](../.cursorrules) |

---

## 1. 작업 개요

| 항목 | 내용 |
|------|------|
| **목적** | 레이어드 패키지 구조(`unit_converter/`)를 SSOT에 고정하고, Phase 0 골격 코드·RED 테스트 설계·스켈레톤까지 반영 |
| **입력** | 아키텍처 다이어그램(domain / app / infrastructure / cli), PRD v0.2, 기존 `UnitConverter.py` |
| **산출물** | `unit_converter/` 패키지, `tests/` 확장, PRD §5.6 개정, `.cursorrules` 갱신, RED 설계·스켈레톤, 본 보고서, Transcript 03, `README.md` |

---

## 2. 설계 원칙 (확정)

| 구분 | 기준 |
|------|------|
| **물리 구조** | 다이어그램 고정 — `domain/`, `app/`, `infrastructure/`, `cli.py`, `tests/test_converter.py`·`test_cli.py` |
| **논리·구현** | PRD Phase·버전 — 파일별 범위 표(§5.6), v0.4 `config_loader` 스텁, v1.0 json/csv 금지 |
| **의존 방향** | `boundary (cli) → app (parser, presenter) → domain (registry, converter)` — A4 |

### 2.1 논리 레이어 ↔ 패키지 매핑

| 논리 (PRD) | 물리 경로 | 대표 모듈 |
|------------|-----------|-----------|
| entity (A1) | `unit_converter/domain/` | `length_unit`, `unit_registry`, `converter` |
| control (A2) | `unit_converter/app/` | `input_parser`, `output_formatter` (= presenter) |
| boundary (A3) | `unit_converter/cli.py` | `run_session`, `main` |
| infrastructure | `unit_converter/infrastructure/` | `config_loader` (v0.4 스텁) |

---

## 3. PRD·cursorrules 변경 요약

### 3.1 PRD (`docs/PRD.md` §5.6)

- 패키지 트리·논리 의존 다이어그램 추가
- 파일별 PRD 범위·Phase 매핑 표 추가
- AC11 표현을 `app` 모듈명(`input_parser`, `output_formatter`)에 정렬
- `UnitConverter.py` → `cli` 위임 하위 호환 명시

### 3.2 `.cursorrules`

- 패키지 경로·진입점(`python -m unit_converter.cli`) 명시
- 테스트 경로: `tests/test_converter.py`, `tests/test_cli.py` + `tests/{entity,control}/`
- 아키텍처 표: 경로별 v0.2 구현 범위

---

## 4. 코드 산출 (Phase 0)

### 4.1 패키지 (`unit_converter/`)

| 모듈 | Phase 0 상태 | PRD |
|------|--------------|-----|
| `domain/unit_registry.py` | meter/feet/yard 내장, 계수 SSOT | D1~D3, CS5 |
| `domain/converter.py` | meter 정규화 → 전 단위 | F1~F2, D4 |
| `domain/length_unit.py` | Protocol 골격 | v0.3 OCP |
| `app/input_parser.py` | `from:value` 파싱 | I1, I3, I4 |
| `app/output_formatter.py` | table 3줄 문자열 | O3, AC1 |
| `cli.py` | `input`/`print` boundary | C1~C2, A3 |
| `infrastructure/config_loader.py` | `NotImplementedError` | v0.4 |

### 4.2 진입점

- [`UnitConverter.py`](../UnitConverter.py) — `unit_converter.cli.main()` 위임
- `python -m unit_converter.cli`

### 4.3 테스트 (현재)

| 파일 | Track | 상태 |
|------|-------|------|
| `tests/test_converter.py` | Logic | GREEN — D 변환, AC2~AC3 |
| `tests/test_cli.py` | UI | GREEN — AC1 3줄 출력 |
| `tests/control/test_d_t5_01.py` | Logic | **RED** — D-T5-01 |
| `tests/entity/test_d_arc_01.py` | Logic | **RED** — D-ARC-01 |
| `tests/control/test_d_arc_02.py` | Logic | **RED** — D-ARC-02 |
| `tests/conftest.py` | — | 픽스처 `g_*` |

```bash
python -m pytest tests/ -v
# 5 passed, 3 failed (RED 스켈레톤 의도)
```

---

## 5. Dual Track RED (Phase 0 잔여)

### 5.1 `/red-test-plan` 묶음

| Test ID | PRD | Then (목표) |
|---------|-----|-------------|
| D-T5-01 | T5, AC11, A2 | app에 `print`/`input`/`tkinter` 0건 |
| D-ARC-01 | A4 | domain이 app/cli import 안 함 |
| D-ARC-02 | A4 | app이 cli import 안 함 |

### 5.2 `/red-skeleton`

- `tests/conftest.py`, `tests/control/`, `tests/entity/` 생성
- Then: `pytest.fail("RED: …")` only — GREEN은 `/green-minimal`에서 AST 검사 구현

---

## 6. 구현 권장 순서 (갱신)

```
0. [진행 중] Phase 0 — 패키지 골격 ✅ / D-T5·D-ARC GREEN ⏳
1. Phase 1 — F4 별칭·trim (D-T1-01, U-T1-01)
2. Phase 2 — F5 목표 1줄 (D-T2-01, U-T2-01)
3. Phase 3 — T3 하위 호환·오류 (AC4~AC6, AC10)
4. Phase 4 — F6·F7 제안·목록
5. Phase 5 — GUI G1~G5, T6
6. Phase 6 — v0.3 OCP registry 전면
```

---

## 7. 리스크

| 항목 | 완화 |
|------|------|
| 다이어그램 파일명 vs PRD 용어(parser/presenter) | §5.6 표로 `input_parser`↔parser, `output_formatter`↔presenter 명시 |
| Phase 0 RED가 즉시 GREEN 가능 | 회귀 가드로 유지, 스켈레톤 후 AST assert 전환 |
| `tests/` 평면·계층 혼재 | Phase 1+에서 `tests/control/` 등으로 점진 이전 |

---

## 8. 참고

- PRD: [`docs/PRD.md`](../docs/PRD.md)
- Transcript: [`Prompts/03_UnitConverter_Architecture-RED-Transcript.md`](../Prompts/03_UnitConverter_Architecture-RED-Transcript.md)
- 이전 보고서: [`03_UnitConverter_Boundary_GUI_Report.md`](./03_UnitConverter_Boundary_GUI_Report.md)
- RED reference: [`.cursor/skills/red-test-plan/reference.md`](../.cursor/skills/red-test-plan/reference.md)
