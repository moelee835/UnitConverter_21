---
name: refactor-smell
description: >-
  UnitConverter ARRR Refactor 코드 스멜 분석만. /refactor-smell,
  pytest 전체 PASS 전제, docs/Code_smell.md 생성·갱신, src/tests 코드 수정 금지,
  Change Budget 내 /refactor-safe 후보 제안.
disable-model-invocation: true
---

# Refactor Smell (ARRR — Refactor · 분석만)

**코드 수정·commit 금지.** `docs/Code_smell.md` 보고서만 생성·갱신.

SSOT: [`.cursorrules`](../../../.cursorrules), [`docs/PRD.md`](../../../docs/PRD.md) §9, [reference.md](reference.md).

## 선행 조건

```bash
python -m pytest tests/ -v
```

- **전부 PASS 아니면 중단** — FAIL 목록 보고, 스멜 스캔·`Code_smell.md` 작성 안 함

## 언제 사용

| 트리거 | 예 |
|--------|-----|
| `/refactor-smell` | GREEN·golden 후 회귀 안전 상태에서 스멜 표 |
| REFACTOR 준비 | `/refactor-safe` 전 |

**사용하지 않을 때:** `src`·`entity`·`control`·`tests` **로직 수정**, git commit(사용자 요청 전).

## 필수 선언 (응답 첫 줄)

```
Phase: refactor | Scope: entity/ control/ boundary/ tests/ UnitConverter.py | Track: Logic+UI
```

## 절차

### 1. pytest 전제

```bash
python -m pytest tests/ -v
```

FAIL → 중단 메시지 후 종료.

### 2. 스캔

대상: `UnitConverter.py`, `entity/`, `control/`, `boundary/`, `tests/` ([reference.md](reference.md)).

카테고리별 **증거** 수집 (grep·읽기):

| 카테고리 | UnitConverter 근거 |
|----------|-------------------|
| Long Method (>25줄·책임2+) | `main()` 등 |
| Duplicated Code | meter↔feet↔yard 변환·print 3줄 반복 (CS6) |
| Mysterious Name | 의도 불명 식별자 |
| Magic Number | `3.28084`/`1.09361` constants 밖 (CS5) |
| ECB 위반 | 역방향 import; entity/control I/O (AC11) — **E001~E007 없음** |
| Feature Envy | boundary·main에 도메인·변환 로직 (CS4) |

PRD **CS ID**를 근거 열에 반드시 연결.

### 3. `docs/Code_smell.md`

| 상황 | 동작 |
|------|------|
| 파일 **없음** | 아래 표 템플릿으로 **신규 생성** |
| 파일 **있음** | 기존 요약 + 이번 스캔 delta; 사용자가 “갱신” 요청 시에만 전체 교체 |

### 4. 보고서 표 템플릿

```markdown
# Code Smell Report — UnitConverter

| 스캔 일시 | YYYY-MM-DD |
| pytest | tests/ 전체 PASS |

## 스멜 목록

| 우선순위 | 스멜 | PRD/CS | 위치(파일:함수) | 근거 | Change Budget 내 /refactor-safe 후보 |
|----------|------|--------|-----------------|------|--------------------------------------|
| P0 | … | CS5 | UnitConverter.py:main | … | 예: constants 추출 (1파일) |
```

- 행이 없으면 `해당 없음` 명시
- **Change Budget:** 파일≤3 · 클래스≤1 · 메서드≤3 — 후보는 Budget **내**만

### 5. 터미널 출력

- P0 / P1 / P2 **요약 표** (스멜·위치·CS)
- **`/refactor-safe` 후보 1~3개** (Budget 내, P0 우선)

### 6. 다음 안내 (한 줄)

`가장 P0 1개(<CS ID>)만 골라 /refactor-safe 실행하세요.`

## 금지

| 금지 | |
|------|--|
| `entity/`·`control/`·`boundary/`·`tests/`·`UnitConverter.py` 수정 | |
| golden 수동 편집 | |
| assert 완화로 PASS 맞추기 | |
| git commit | |

## ARRR 체인

`/golden-master` (또는 GREEN stable) → `/refactor-smell` → [`/refactor-safe`](../refactor-safe/SKILL.md)
