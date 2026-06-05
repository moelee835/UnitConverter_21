# 03. UnitConverter Architecture·Package·RED — Prompt Export Transcript

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_21 |
| 작성일 | 2026-06-05 |
| 세션 | 패키지 아키텍처 반영 · Phase 0 구현 · RED 설계·스켈레톤 |

---

## Turn 1 — User

```
위 아키텍처를 PRD, .Cursorrules, 그리고 현재 프로젝트 리포지토리에 반영할 것.
```

(첨부: `unit_converter/` 레이어드 구조 다이어그램 — domain, infrastructure, app, cli, tests)

## Turn 1 — Assistant (요약)

- `docs/PRD.md` §5.6 — 패키지 트리·논리 매핑·파일별 PRD 범위 표
- `.cursorrules` — 패키지 경로·의존 방향·테스트 경로
- `unit_converter/` 패키지 생성 (domain, app, infrastructure, cli)
- `UnitConverter.py` → `cli.main()` 위임
- `tests/test_converter.py`, `tests/test_cli.py` — pytest 5 passed
- `README.md` 아키텍처 절 갱신

---

## Turn 2 — User

```
위 아키텍처 구조는 그대로 따르되, py 파일 등은 PRD 기준으로
```

## Turn 2 — Assistant (요약)

- **물리 트리 고정**, **구현 범위는 PRD Phase/버전**
- `output_formatter` — v0.2 table만; json/csv는 v1.0
- `config_loader` — v0.4 스텁
- PRD §5.6 파일별 Phase 표로 정렬

---

## Turn 3 — User

```
/red-test-plan
```

## Turn 3 — Assistant (요약)

- **Ask 모드** — 코드 생성 없음
- 선언: `Phase: red | Layer: entity+control | Track: Logic`
- 이번 RED 묶음: **D-T5-01, D-ARC-01, D-ARC-02** (Phase 0, T5, AC11, A4)
- 4섹션: C2C · RED 표 · 테스트 플랜 · ECB·Mock
- 완료: `/red-skeleton` 가능

---

## Turn 4 — User

```
/red-skeleton
```

## Turn 4 — Assistant (요약)

- `tests/conftest.py` — `g_meter_2_5`, `g_meters_typo`, `g_to_yard`, `g_app_module_names`, `g_domain_module_names`
- `tests/control/test_d_t5_01.py`
- `tests/entity/test_d_arc_01.py`
- `tests/control/test_d_arc_02.py`
- Then: `pytest.fail("RED: …")` only
- pytest: **3 failed** (의도적 RED)

---

## Turn 5 — User

```
Reports/ 아래 리포트 생성, prompt Transcript 완료 후, READMD.md 까지 수정
```

## Turn 5 — Assistant (요약)

- `Reports/04_UnitConverter_Architecture_Package_Report.md` 작성
- `Prompts/03_UnitConverter_Architecture-RED-Transcript.md` 작성 (본 문서)
- `README.md` — v0.2 Phase 0 상태, 실행·pytest, 문서 링크 갱신
- `docs/PRD.md` §12 참고 링크 추가

---

## 산출물 목록

| 경로 | 설명 |
|------|------|
| `unit_converter/` | 레이어드 패키지 (Phase 0) |
| `docs/PRD.md` | §5.6 패키지 SSOT |
| `.cursorrules` | 패키지·테스트·Phase |
| `tests/conftest.py` | 공통 픽스처 |
| `tests/control/test_d_t5_01.py` | RED D-T5-01 |
| `tests/entity/test_d_arc_01.py` | RED D-ARC-01 |
| `tests/control/test_d_arc_02.py` | RED D-ARC-02 |
| `Reports/04_UnitConverter_Architecture_Package_Report.md` | 본 세션 보고서 |
| `Prompts/03_UnitConverter_Architecture-RED-Transcript.md` | 본 Transcript |
| `README.md` | 실행·TC·문서 링크 |

---

## Test ID Quick Reference (본 세션)

| ID | Layer | 상태 |
|----|-------|------|
| D-T5-01 | control (app) | RED 스켈레톤 |
| D-ARC-01 | entity (domain) | RED 스켈레톤 |
| D-ARC-02 | control (app) | RED 스켈레톤 |
| (기존) test_converter | domain | GREEN |
| (기존) test_cli | boundary | GREEN |

---

## 다음 Command

| Command | 목표 |
|---------|------|
| `/green-minimal` | D-T5-01, D-ARC-01, D-ARC-02 AST 검사 GREEN |
| `/red-test-plan` | Phase 1 — D-T1-01, U-T1-01 (F4, T1, AC7) |
