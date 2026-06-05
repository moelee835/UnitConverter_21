# Refactor Smell — PRD CS · 스캔 범위

## 스캔 대상 경로

```
UnitConverter.py          # legacy boundary+logic (v0.1)
entity/
control/
boundary/
tests/
```

`src/` 없음. MagicSquare `int[6]`·E001~E007 **미적용**.

## PRD 코드 스멜 ID (§9 + 역분석 CS1~CS18)

| ID | 스멜 | Mom Test | v0.2 우선 |
|----|------|----------|-----------|
| CS1 | God Function / SRP | — | A1~A5 |
| CS3 | OCP — if-elif 단위 | — | P0 |
| CS4 | I/O in main | — | P0 |
| CS5 | Magic Number | — | P0 |
| CS6 | 중복 변환 로직 | — | P0 |
| CS8 | 음수 미검증 | — | P1 |
| CS9 | No trim | S3, S4 | P1 |
| CS10 | Primitive Obsession | S4 | P0 |
| CS12 | 출력 명명·형식 | — | P2 |
| CS13 | Raw float | S9 | P1 |
| CS14 | Hard-coded 3줄 출력 | S7, S8 | P0 |

## 탐지 카테고리 → CS 매핑

| 카테고리 | 탐지 기준 | CS |
|----------|-----------|-----|
| Long Method | `main()` 또는 함수 >25줄·책임 2+ | CS1, CS4 |
| Duplicated Code | to_meter / from_meter·print 3줄 반복 | CS5, CS6 |
| Mysterious Name | `in_meters`, `value_str` 등 의도 불명 | CS1 |
| Magic Number | `3.28084`, `1.09361`이 `entity/constants` 밖 | CS5 |
| ECB 위반 | 역방향 import; entity/control `print`/`input`/tkinter | CS4, AC11 |
| Feature Envy | boundary·`main()`에 파싱·변환·포맷 | CS4, CS10 |

## Change Budget (`/refactor-safe` 공통)

| 항목 | 한도 |
|------|------|
| 파일 | ≤ 3 |
| 클래스 | ≤ 1 |
| 메서드 | ≤ 3 |

후보 제안 시 Budget 초과 항목은 **P2로 강등** 또는 분할 제안.

## `docs/Code_smell.md`

- **없음** → 본 스캔 결과로 **신규 생성**
- **있음** → 재스캔 후 diff 요약만; 전체 덮어쓰기는 사용자 지시 시

## 우선순위 가이드

| P0 | Mom Test·AC 직결, TC 불가, OCP/ECB 핵심 |
| P1 | trim·float·음수·SRP |
| P2 | 명명·포맷·문서화 수준 |
