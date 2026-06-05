# 01. UnitConverter Spec — Prompt Export Transcript

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_21 |
| 브랜치 | spec |
| 작성일 | 2026-06-05 |
| 세션 | spec — 요구사항 분석 · Mom Test · PRD 반영 |

---

## Turn 1 — User

```
현재 프로젝트에 존재하는 @UnitConverter.py 를 읽고, 이 파이썬 코드를 통해 구현하려고 했던 요구사항을 md 파일로 출력하라. 양식은 @PRD.md 파일을참고하고 docs/ 디렉터리 아래에 출력해.

주요 리뷰 사항 : 현재 코드에 존재하는 코드 스멜들을 분석하고 해당 사항도 기록하시오.
```

## Turn 1 — Assistant (요약)

- `UnitConverter.py`, `README.md` 역분석
- PRD 양식으로 `docs/UnitConverter_Requirements_FromCode.md` 작성 (후 `docs/PRD.md`로 통합)
- 코드 스멜 CS1~CS18 분석 (OCP 위반, Magic Number, SRP, I/O 결합 등)

---

## Turn 2 — User

```
[Mom Test 원칙 이미지]

본 프로젝트 요구사항 분석 결과를 토대로 Mom test를 진행한다. 
제공되는 Mom test 원칙을 읽고 나에게 질문해
```

## Turn 2 — Assistant (요약)

- Mom Test 3원칙 (아이디어 X, 과거 사실, 칭찬/미래 의견 X)
- 페르소나 A~D 제시, Q1~Q5 질문 세트 제공

---

## Turn 3 — User

```
하나씩 차례로 질문해
```

## Turn 3 — Assistant

- 페르소나 선택 요청 (A/B/C/D)

---

## Turn 4 — User

```
B
```

## Turn 4 — Assistant — Mom Test Q1

**질문:** meter/feet/yard를 마지막으로 변환했을 때? 무엇을, 어떤 도구로?

---

## Turn 5 — User

```
오늘 아침.(26-06-05), meter를 yard로 변환하려 했고 UnitConverter.py 프로그램을 쓰려했음
```

## Turn 5 — Assistant — Mom Test Q2

**질문:** 가장 번거로웠던 순간?

---

## Turn 6 — User

```
meter를 직접 타이핑해야했고, 잘못 타이핑 meters로 해서 Unkown unit이 출력됨
```

## Turn 6 — Assistant — Mom Test Q3

**질문:** 오류 인지 시점? 몇 분 추가?

---

## Turn 7 — User

```
출력을 보고 나서
```

## Turn 7 — Assistant — Mom Test Q4

**질문:** 여러 단위 동시 확인 필요? 각각 vs 한 번에?

---

## Turn 8 — User

```
3번질문에 대략 5분 추가 답변.

그리고 자주 있었음. yard든 feet든 다 출력할 필요는 없었음. 원하는거 선택하는게 필요함. meter - yard 변환하여 해외 발신용 메일을 작성해야 했기 때문임.
```

## Turn 8 — Assistant — Mom Test Q5

**질문:** 변환 계수 어디서 확인?

---

## Turn 9 — User

```
프로그램 출력을 그대로 신뢰
```

## Turn 9 — Assistant (요약)

- Evidence S1~S9 정리
- Problem Statement: 오타 → Unknown → ~5분, 목표 단위 선택 필요
- PRD 후보: F4 별칭, F5 선택 출력, F6 제안

---

## Turn 10 — User

```
이 내용을 PRD.md + .cursorrules로 반영하고 Mom Test 보고서도 docs 아래 출력해.
```

## Turn 10 — Assistant (요약)

- `docs/PRD.md` v0.2 (Mom Test 반영)
- `.cursorrules` UnitConverter 전용 규칙
- `docs/UnitConverter_MomTest_Report.md` 생성

---

## Turn 11 — User

```
Reports/ 아래에 01_, 02_ 네이밍 규칙을 부여하여 이번 작업 리포트 생성, Prompt Transcript도 출력해줘 (Prompts/ 아래에). 그리고 spec 브랜치(현재)를 push
```

## Turn 11 — Assistant

- `Reports/01_UnitConverter_ProblemDefinition_Report.md`
- `Reports/02_UnitConverter_MomTest_Report.md`
- `Prompts/01_UnitConverter_Spec-Export-Transcript.md` (본 문서)
- spec 브랜치 commit & push

---

## 산출물 목록

| 경로 | 설명 |
|------|------|
| `docs/PRD.md` | PRD v0.2 (역분석 + Mom Test) |
| `docs/UnitConverter_MomTest_Report.md` | Mom Test Q&A 상세 |
| `.cursorrules` | Cursor Agent 규칙 |
| `Reports/01_UnitConverter_ProblemDefinition_Report.md` | 코드 역분석 보고서 |
| `Reports/02_UnitConverter_MomTest_Report.md` | Mom Test 요약 보고서 |
| `Prompts/01_UnitConverter_Spec-Export-Transcript.md` | 본 Transcript |

---

## Evidence Quick Reference

| ID | 한 줄 요약 |
|----|-----------|
| S4 | `meters` → Unknown unit |
| S6 | ~5분 재작업 |
| S7·S8 | 목표 단위만 필요, 자주 |
