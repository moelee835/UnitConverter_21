# /refactor-smell — ARRR Refactor · 코드 스멜 분석 (수정 금지)

UnitConverter — **pytest 전체 PASS** 후 `src`·`tests`·패키지 **스캔만**.  
`.cursorrules`, `.cursor/skills/refactor-smell/SKILL.md`, `docs/PRD.md` §9.

**허용 출력:** `docs/Code_smell.md` 생성·갱신 · 터미널 표  
**금지:** 코드 수정 · commit (사용자 요청 전)

---

## 필수 선언 (응답 첫 줄)

```
Phase: refactor | Scope: entity/ control/ boundary/ tests/ UnitConverter.py | Track: Logic+UI
```

---

## 전제 확인 (중단 조건)

```bash
python -m pytest tests/ -v
```

- **전부 PASS 아니면** 중단 — FAIL 테스트·파일 보고, 스멜 스캔·`Code_smell.md` **작성 안 함**
- `tests/` 없으면: “테스트 하네스 없음 — GREEN 선행” 안내

---

## 절차

1. pytest 전체 PASS 확인  
2. `UnitConverter.py`, `entity/`, `control/`, `boundary/`, `tests/` 스캔 (**코드 수정 금지**)  
3. `docs/Code_smell.md` — **없으면 생성**, **있으면** 기존 파악 후 delta·요약(전체 덮어쓰기는 사용자 지시 시)  
4. 터미널에 P0/P1/P2 표 + `/refactor-safe` 후보 1~3개  
5. **다음 안내:** 가장 P0 1개만 골라 `/refactor-safe` 실행

---

## 스멜 표 (보고서·출력 공통)

| 우선순위 | 스멜 | PRD/CS | 위치(파일:함수) | 근거 | Change Budget 내 리팩터 후보 |
|----------|------|--------|-----------------|------|------------------------------|
| P0/P1/P2 | Long Method (>25줄·책임2+) | CS1, CS4 | | | |
| | Duplicated Code (변환·출력 이중) | CS5, CS6 | | | |
| | Mysterious Name | CS1 | | | |
| | Magic Number (`3.28084`/`1.09361` constants 밖) | CS5 | | | |
| | ECB 위반 (역방향 import·control/entity I/O) | CS4, AC11 | | | |
| | Feature Envy (boundary·main에 도메인 로직) | CS4, CS10 | | | |
| | Hard-coded 3줄 출력 | CS14 | | | |
| | No trim / Primitive Obsession | CS9, CS10 | | | |
| | Raw float 출력 | CS13 | | | |

MagicSquare **E001~E005** · **int[6]** · **34/16/4** — **본 프로젝트 미사용**.

---

## Change Budget (`/refactor-safe`와 동일)

| 항목 | 한도 |
|------|------|
| 파일 | ≤ 3 |
| 클래스 | ≤ 1 |
| 메서드 | ≤ 3 |

후보는 Budget **초과 제안 금지** — 초과 시 분할·다음 스프린트로 표기.

---

## `docs/Code_smell.md`

- 경로: `docs/Code_smell.md`
- **신규:** 스캔 일시, pytest 결과, 위 표 전체, Mom Test 연결(S1~S9·CS)
- **기존:** 상단 “이번 스캔 delta” 절 추가 권장

---

## 호출 예시 (사용자 메시지)

```
/refactor-smell
Phase: refactor | Scope: entity/ control/ boundary/ tests/ | Track: Logic+UI
전제 확인:
python -m pytest tests/ -v
→ 전부 PASS 아니면 중단하고 알려줘.
다음 스멜 표로 스캔 (코드 수정·commit 금지):
docs/Code_smell.md 생성 (있으면 delta만).
Change Budget: 파일≤3 · 클래스≤1 · 메서드≤3
출력: P0/P1/P2 표 + /refactor-safe 후보 1~3개 (Budget 내)
다음: 가장 P0 1개만 골라 /refactor-safe 실행하라고 안내.
```

---

## 터미널 보고 형식

```markdown
## Refactor Smell 보고

- **pytest:** N passed (전체 PASS)
- **Code_smell.md:** 생성 | delta 갱신 | (경로)
- **P0:** (요약 1~3행)
- **P1/P2:** (요약)
- **/refactor-safe 후보:** 1) … 2) … 3) …
- **다음:** P0 `<CS ID>` 1개만 `/refactor-safe`
```

---

## 금지

| 금지 | |
|------|--|
| 소스·테스트 코드 패치 | |
| `Code_smell.md` 없이 “통과” 주장 | |
| pytest FAIL 무시하고 스캔 | |
| golden 수동 편집 권장 | |
| git commit | |

---

## ARRR Command 체인

| # | Command |
|---|---------|
| 1~4 | `/red-test-plan` … `/golden-master` |
| 5 | **`/refactor-smell`** (본 Command) |
| 6 | [`/refactor-safe`](../commands/refactor-safe.md) |
