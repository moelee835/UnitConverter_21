---
name: refactor-safe
description: >-
  UnitConverter ARRR Refactor 안전 개선. /refactor-safe,
  refactor-smell에서 선택한 스멜 1개, Change Budget, pytest·golden 회귀,
  입출력 계약 불변, 기능 추가 금지.
disable-model-invocation: true
---

# Refactor Safe (ARRR — Refactor · 적용)

`/refactor-smell` 표에서 **선택한 스멜 1개**만 Change Budget 내에서 구조 개선.

SSOT: [`.cursorrules`](../../../.cursorrules), [`docs/Code_smell.md`](../../../docs/Code_smell.md), [refactor-smell/reference.md](../refactor-smell/reference.md), [reference.md](reference.md).

## 선행 조건

1. `docs/Code_smell.md` 존재 (없으면 `/refactor-smell` 먼저)
2. ```bash
   python -m pytest tests/ -v
   ```
   **전부 PASS**
3. 사용자가 **스멜 1개·대상 파일·Budget** 명시

## 필수 선언 (응답 첫 줄)

```
Phase: refactor | Scope: <대상 경로> | Track: Logic+UI
스멜: <이름> (CSx) | Budget: 파일≤N · 메서드≤M
```

## Change Budget (초과 금지)

| 항목 | 한도 |
|------|------|
| 파일 | ≤ 3 |
| 클래스 | ≤ 1 |
| 메서드 | ≤ 3 (extract·move 합산) |

초과 시 **이번 턴 중단** — 분할안만 제안.

## 원칙 (동작 불변)

| 원칙 | UnitConverter |
|------|----------------|
| 입출력 계약 | O3 포맷, AC1 3줄·AC8 1줄 **문자열 동일** (리팩터만) |
| int[6]·격자 | **해당 없음** |
| entity | **E001~E007 없음** — entity에 사용자 메시지·`print`/`input` **추가 금지** |
| ECB | `boundary → control → entity`; 역방향 import 금지 |
| 테스트 | assert 완화 · skip · xfail **금지** |
| 범위 | **기능 추가·버그 수정 금지** — 별도 `/green-minimal` |

## 절차

### 1. 스멜·Budget 확인

- `Code_smell.md` 해당 행과 일치하는지 확인
- 이번 턴 **한 CS·한 후보**만

### 2. 최소 리팩터

- Extract Method / 상수 SSOT(`entity/constants.py`) / 모듈 분리 등
- **테스트 assert·golden 포맷 키** 변경 금지 (필요 시 의도적 golden 절차)

### 3. pytest 전체

```bash
python -m pytest tests/ -v
```

- FAIL → 즉시 수정 또는 **롤백** 후 보고

### 4. Golden (있을 때)

```bash
python -m pytest tests/control/test_d_t2_01.py -v
# UPDATE_GOLDEN 설정 없음
```

| 결과 | 조치 |
|------|------|
| **matched** | OK |
| **diff 비의도** | 리팩터 **롤백** |
| **diff 의도** (포맷·LF·문서화된 반올림) | `Reports/` 또는 PRD 근거 1줄 + `UPDATE_GOLDEN=1` 재실행 |

`tests/golden/` 없으면: “golden N/A — full pytest만” 명시.

### 5. `Code_smell.md` delta (선택)

- 해결한 행에 `✅ refactor-safe YYYY-MM-DD` — **사용자 요청 시**

### 6. 보고

- 변경 요약 (파일·메서드·Budget 사용량)
- pytest: N passed
- golden: matched | N/A | UPDATE_GOLDEN 재생성(의도)

**git commit:** 사용자 요청 시만.

## 호출 예시 (CS6)

```
/refactor-safe
스멜: Duplicated Code (CS5, CS6)
대상: UnitConverter.py:main — to_meter / meter→feet·yard
Budget: 파일 2 · 메서드 2 (to_meter, from_meter)
→ entity/constants.py + control/converter.py
```

## 금지

| 금지 | |
|------|--|
| 스멜 2개 이상 동시 | |
| Budget 초과 | |
| F4 별칭·F5 1줄 등 **신규 기능** | |
| RED/GREEN Phase 혼합 | |
| golden 수동 편집 | |

## ARRR 체인

`/refactor-smell` → **`/refactor-safe`** (본 skill)
