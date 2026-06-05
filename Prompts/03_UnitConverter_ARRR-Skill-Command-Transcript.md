# 03. UnitConverter ARRR · Skill · Command — Prompt Export Transcript

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_21 |
| 브랜치 | spec |
| 작성일 | 2026-06-05 |
| 세션 | spec — Dual Track TDD · `.cursorrules` · ARRR Skill·Command 6쌍 |

---

## Turn 1 — User

```
Dual Track TDD가 뭔지 설명해줘
```

## Turn 1 — Assistant (요약)

- Discovery(문제·AC·Mom Test) vs Delivery(`tests/` Red→Green→Refactor) 두 트랙 설명
- UnitConverter: PRD §6, S1~S9, T1~T6, `.cursorrules` 연결

---

## Turn 2 — User

```
Dual track tdd 시 사용할 cursor.ai 기술 몇가지 예시를 작성하고 실행 방법을 알려줘. 한국어로
```

## Turn 2 — Assistant (요약)

- `@` SSOT, Ask/Agent, `.cursorrules`, `.cursor/rules/`, Phase/Tn 프롬프트
- 예상 스킬 맵: discovery / delivery / 연결

---

## Turn 3 — User

```
.cursorrules 체크해서 Dual Track TDD를 수행하기에 문제 없는지 체크
```

## Turn 3 — Assistant (요약)

- **대체로 충분**, AC11/T5 불일치·T1~T6 누락·Phase vs TDD 순서 모호 지적
- 보강 권장 5항목 제시

---

## Turn 4 — User

```
권장 사항을 cursorrules에 반영해줘
```

## Turn 4 — Assistant (요약)

- Agent 모드: Dual Track 섹션, Phase 표, T1~T6, T5 P0, Mom Test 확인 목록, AC7 해석 추가

---

## Turn 5 — User

```
이제 cursor에서 사용할 skill들을 구성할 텐데… 하나씩 던져줄거고 그에따라 작업
```

## Turn 5 — Assistant (요약)

- 프로젝트 `.cursor/skills/`, Command 체인, SSOT·프롬프트 포함 가이드
- 첫 프롬프트 대기

---

## Turn 6 — User (Skill 1)

```
1. ARRR Ask — Test RED 생성. "/red-test-plan", skill + command
```

(기획→설계→RED 설계, Rule 1~3, RED 금지, UI/Logic RED 설계표, `/red-test-plan` 호출 예시 포함)

## Turn 6 — Assistant (요약)

- `.cursor/skills/red-test-plan/` + `.cursor/commands/red-test-plan.md`
- UnitConverter: D-*/U-*, T1~T6, `entity/`·`control/`·`boundary/`

---

## Turn 7 — User (Skill 2)

```
2. ARRR Ask — Test RED Skeleton. "/red-skeleton", skill + command
```

## Turn 7 — Assistant (요약)

- `red-skeleton` Skill·Command, `pytest.fail` AAA, `tests/`만

---

## Turn 8 — User (Skill 3)

```
3. ARRR Respond — 최소 Green. "/green-minimal", skill + command
```

## Turn 8 — Assistant (요약)

- `green-minimal` Skill·Command, Budget 1 Test ID, ECB·constants SSOT

---

## Turn 9 — User (Skill 4)

```
4. ARRR Respond — Test Golden 구축. "/golden-master", skill + command
```

## Turn 9 — Assistant (요약)

- `golden-master`, `tests/_approval.py`, `UPDATE_GOLDEN=1`, UnitConverter 텍스트 golden 포맷

---

## Turn 10 — User (Skill 5)

```
5. ARRR Refactor — 코드 스멜 탐지. "/refactor-smell", skill + Command
```

(`/refactor-smell` 실행 — Cursor Command 붙여넣기)

## Turn 10 — Assistant (요약)

- `refactor-smell`, `docs/Code_smell.md`, pytest PASS 전제, P0→`/refactor-safe` 안내

---

## Turn 11 — User (Skill 6)

```
6. ARRR Refactor — 코드 스멜 개선. "/refactor-safe", skill + Command
```

## Turn 11 — Assistant (요약)

- `refactor-safe`, Change Budget, golden matched·롤백 정책, CS6 예시 매핑

---

## Turn 12 — User

```
Report/ 아래 리포트 생성, Prompt Transcript 하고 spec 브랜치 push
```

## Turn 12 — Assistant (예정)

- `Reports/04_UnitConverter_ARRR-Skill-Command-보고서.md`
- `Prompts/03_UnitConverter_ARRR-Skill-Command-Transcript.md`
- `spec` commit · push

---

## 산출물 경로 (세션 최종)

| 유형 | 경로 |
|------|------|
| Rule | `.cursorrules` |
| Skill ×6 | `.cursor/skills/{red-test-plan,red-skeleton,green-minimal,golden-master,refactor-smell,refactor-safe}/` |
| Command ×6 | `.cursor/commands/*.md` |
| Report | `Reports/04_UnitConverter_ARRR-Skill-Command-보고서.md` |
| Transcript | `Prompts/03_UnitConverter_ARRR-Skill-Command-Transcript.md` |

---

## 다음 권장 Command (실행 순)

```text
/red-test-plan  →  /red-skeleton  →  /green-minimal  →  /golden-master
  →  /refactor-smell  →  /refactor-safe
```

첫 실행 예: `Phase: red | Layer: control | Track: Logic` · `D-T1-01 (F4, T1, AC7)`
