# 01. UnitConverter 문제 정의 보고서 (코드 역분석)

| 항목 | 내용 |
|------|------|
| 제품 | UnitConverter — 길이 단위 변환 CLI |
| 작성일 | 2026-06-05 |
| 브랜치 | spec |
| 상태 | Complete |
| 연계 | [`docs/PRD.md`](../docs/PRD.md) |

---

## 1. 작업 개요

| 항목 | 내용 |
|------|------|
| **목적** | [`UnitConverter.py`](../UnitConverter.py) 코드 역분석 → 구현·암시 요구사항 PRD화 |
| **입력** | `UnitConverter.py`, `README.md`, PRD 양식 참조 |
| **산출물** | `docs/PRD.md` (v0.1 역분석), 코드 스멜 목록 (CS1~CS18) |

---

## 2. 분석 대상 코드 요약

```python
# UnitConverter.py — 37줄, main() 단일 함수
# 입력: unit:value → meter 기준 정규화 → meter/feet/yard 3줄 출력
```

| 영역 | 현재 구현 |
|------|-----------|
| 입력 | `input()` 대화형, `unit:value` |
| 지원 단위 | meter, feet, yard (if-elif) |
| 변환 | meter 기준, 계수 3.28084 / 1.09361 |
| 출력 | 3개 `print` 고정 |
| 검증 | `:`, float, 화이트리스트 |

---

## 3. 역분석 요구사항 (핵심)

### 3.1 도메인

- **D1~D4:** meter 기준 3단위 변환
- **I1~I5:** `unit:value` 형식, 오류 시 메시지 후 종료
- **O1~O3:** 전 단위 3줄 출력 (입력 단위 포함)

### 3.2 README 대비 갭

| README 목표 | 코드 상태 |
|-------------|-----------|
| OCP (단위 추가 최소 변경) | ❌ if-elif |
| SRP (클래스 분리) | ❌ God Function |
| TC (pytest) | ❌ 없음 |
| 음수 검증 | ❌ |
| 설정 외부화 / cubit / JSON·CSV | ❌ |

---

## 4. 코드 스멜 분석 요약

| 우선순위 | ID | 스멜 | 핵심 |
|----------|-----|------|------|
| P0 | CS3 | Open-Closed 위반 | 단위 추가 시 main 수정 |
| P0 | CS4 | 테스트 불가 | I/O·로직 결합 |
| P0 | CS5·CS6 | Magic Number·중복 | 3.28084, 1.09361 이중 |
| P1 | CS1 | SRP / God Function | 파싱·변환·출력 한곳 |
| P1 | CS9·CS10 | 입력 sanitization 부재 | trim·별칭 없음 |
| P2 | CS12·CS13 | 출력 일관성 | 복수형·float 포맷 |
| P2 | CS14 | Hard-coded 출력 | 3줄 print 고정 |

상세: [`docs/PRD.md` §9](../docs/PRD.md)

---

## 5. Acceptance Criteria (코드 기준)

| ID | 시나리오 | 기대 |
|----|----------|------|
| AC1 | `meter:2.5` | 3줄 출력 |
| AC4 | `abc:1` | Unknown unit |
| AC5 | `meter:abc` | Invalid number |
| AC6 | `meter2.5` | Invalid format |

---

## 6. 결론 및 후속

1. **v0.1 상태:** 동작하는 MVP이나 README 품질 목표 미달.
2. **다음 단계:** Mom Test로 진짜 문제 검증 → PRD v0.2 보강.
3. **리팩터 방향:** registry + Parser/Converter/Presenter 분리 (v0.3).

---

## 7. 참고

- PRD: [`docs/PRD.md`](../docs/PRD.md)
- Mom Test: [`02_UnitConverter_MomTest_Report.md`](./02_UnitConverter_MomTest_Report.md)
- Transcript: [`Prompts/01_UnitConverter_Spec-Export-Transcript.md`](../Prompts/01_UnitConverter_Spec-Export-Transcript.md)
