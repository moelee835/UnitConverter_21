# 04. UnitConverter ARRR · Skill · Command 보고서

| 항목 | 내용 |
|------|------|
| 제품 | UnitConverter — 길이 단위 변환 (CLI + GUI v0.2) |
| 작성일 | 2026-06-05 |
| 브랜치 | spec |
| 상태 | Complete — Dual Track `.cursorrules` + ARRR Skill·Command 6쌍 |
| 선행 문서 | [`03_UnitConverter_Boundary_GUI_Report.md`](03_UnitConverter_Boundary_GUI_Report.md), [`docs/PRD.md`](../docs/PRD.md), [`.cursorrules`](../.cursorrules) |

---

## 1. 목적

Boundary·GUI Spec(보고서 03) 이후, **Dual Track TDD**를 Cursor에서 반복 실행할 수 있도록 **ARRR 6단계** Skill·Command를 프로젝트에 고정한다.

| 목표 | 내용 |
|------|------|
| Discovery | PRD → To-Do → Test Case (코드 없음) |
| Delivery | RED skeleton → GREEN minimal → Golden master |
| Refactor | 스멜 분석만 → Budget 1스멜 안전 개선 |
| SSOT | Mom Test S1~S9, T1~T6, Phase 0~5, ECB `entity/`·`control/`·`boundary/` |

**코드·테스트 본문:** 아직 없음 — `UnitConverter.py` v0.1 단일 파일만 존재.

---

## 2. `.cursorrules` 보강 (Dual Track)

| 추가 섹션 | 역할 |
|-----------|------|
| Dual Track TDD | Ask(Discovery) vs Agent(Delivery), SSOT 갱신 순서 |
| v0.2 구현 Phase 표 | Phase 0~6, Tn·AC 매핑 |
| TDD §5.5 | T1~T6 Test Loop, Red→Green 순서 |
| AC7 해석 | 별칭 성공 또는 제안 — Unknown만 금지 |
| T5/AC11 | v0.2 최소 분리 후 control I/O 금지 (P0) |

PRD §5.5·§5.6과 **AC11 시점 불일치** 해소 (이전 점검 피드백 반영).

---

## 3. 산출물 — Skill (6)

| Skill | ARRR | 역할 |
|-------|------|------|
| [`red-test-plan`](../.cursor/skills/red-test-plan/SKILL.md) | Ask | C2C·RED 설계표, `tests/` 생성 금지 |
| [`red-skeleton`](../.cursor/skills/red-skeleton/SKILL.md) | Ask→Delivery | `pytest.fail` RED 골격, `tests/`만 |
| [`green-minimal`](../.cursor/skills/green-minimal/SKILL.md) | Respond | Test ID 1개 최소 GREEN |
| [`golden-master`](../.cursor/skills/golden-master/SKILL.md) | Respond | PASS 후 `tests/golden/*.approved.txt` |
| [`refactor-smell`](../.cursor/skills/refactor-smell/SKILL.md) | Refactor | `docs/Code_smell.md`, 수정 금지 |
| [`refactor-safe`](../.cursor/skills/refactor-safe/SKILL.md) | Refactor | Budget 1스멜, pytest·golden 회귀 |

각 Skill에 `reference.md` (red-test-plan, red-skeleton, green-minimal, golden-master, refactor-smell, refactor-safe).

---

## 4. 산출물 — Command (6)

| Command | 대응 Skill |
|---------|------------|
| [`/red-test-plan`](../.cursor/commands/red-test-plan.md) | red-test-plan |
| [`/red-skeleton`](../.cursor/commands/red-skeleton.md) | red-skeleton |
| [`/green-minimal`](../.cursor/commands/green-minimal.md) | green-minimal |
| [`/golden-master`](../.cursor/commands/golden-master.md) | golden-master |
| [`/refactor-smell`](../.cursor/commands/refactor-smell.md) | refactor-smell |
| [`/refactor-safe`](../.cursor/commands/refactor-safe.md) | refactor-safe |

---

## 5. ARRR Command 체인

```text
/red-test-plan → /red-skeleton → /green-minimal → /golden-master
  → /refactor-smell → /refactor-safe
```

| 단계 | Phase 선언 | 산출물 |
|------|------------|--------|
| 1 | `Phase: red` | RED 설계표, C2C |
| 2 | `Phase: red` | `tests/**` FAIL |
| 3 | `Phase: green` | `entity/`·`control/` 최소 구현 |
| 4 | `Phase: green` | golden baseline |
| 5 | `Phase: refactor` | `docs/Code_smell.md` |
| 6 | `Phase: refactor` | Budget 내 리팩터 |

---

## 6. UnitConverter vs MagicSquare 템플릿 매핑

| MagicSquare | UnitConverter |
|-------------|----------------|
| `int[6]` 1-index golden | `input`/`status`/`lines`/`line_count` 텍스트 계약 |
| E001~E007 boundary | Unknown unit·형식 오류 — boundary/control |
| `src/entity/` | 루트 `entity/`, `control/`, `boundary/` |
| D-LOC / D-SOL | D-T1~T6 (PRD §5.5) |
| 34/16/4 constants | `3.28084` / `1.09361` (`entity/constants.py`) |

---

## 7. Test ID 시드 (reference)

| Tn | Logic `D-*` | UI `U-*` |
|----|-------------|----------|
| T1 | D-T1-01 별칭 | U-T1-01 CLI |
| T2 | D-T2-01 yard 1줄 | U-T2-01 |
| T5 | D-T5-01 import I/O | — |
| T6 | D-T6-01 | U-T6-01 CLI=GUI |

상세: [`.cursor/skills/red-test-plan/reference.md`](../.cursor/skills/red-test-plan/reference.md)

---

## 8. 8계층 · 마무리 점검

| 계층 | 상태 | 근거 |
|------|------|------|
| Rule | ✅ | `.cursorrules` Dual Track·Phase·T1~T6 |
| Skill | ✅ | ARRR 6 Skill + reference |
| Command | ✅ | ARRR 6 Command |
| Harness | ❌ | `tests/`·`pytest` 미구성 |
| Test Loop | ⚠️ | 문서·Command ✅, 실행 0건 |
| Hook | ❌ | 없음 |

**권고:** Phase 0 — `tests/conftest.py` + D-T5-01 또는 T1 RED skeleton → `/green-minimal` 첫 실행.

---

## 9. 의도적으로 하지 않은 것

| 항목 | 이유 |
|------|------|
| `tests/`·`entity/` 구현 | Skill·Command만 본 세션 |
| `docs/Code_smell.md` 실스캔 | `/refactor-smell` 실행 전 |
| 통합 Skill `unitconverter-arr-tdd` | 6쌍 분리 유지 (필요 시 추가) |
| git commit (세션 중) | 사용자 push 요청 시 일괄 |

---

## 10. 다음 단계

1. **Phase 0** — A1~A5 골격 + `/red-test-plan` → `/red-skeleton` (D-T5-01 또는 T1)
2. **Mom Test 우선** — T1 → T2 → T3 (`.cursorrules`)
3. **`/refactor-smell`** — GREEN·golden stable 후 `Code_smell.md` (CS5·CS6·CS4 P0)

---

## 11. 참고

| 경로 | 설명 |
|------|------|
| [`Prompts/03_UnitConverter_ARRR-Skill-Command-Transcript.md`](../Prompts/03_UnitConverter_ARRR-Skill-Command-Transcript.md) | 본 세션 Export |
| [`01_UnitConverter_ProblemDefinition_Report.md`](01_UnitConverter_ProblemDefinition_Report.md) | CS1~CS18 |
| [`02_UnitConverter_MomTest_Report.md`](02_UnitConverter_MomTest_Report.md) | Mom Test 요약 |
