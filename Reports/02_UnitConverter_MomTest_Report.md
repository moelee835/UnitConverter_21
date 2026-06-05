# 02. UnitConverter Mom Test 보고서

| 항목 | 내용 |
|------|------|
| 제품 | UnitConverter — 길이 단위 변환 CLI |
| 작성일 | 2026-06-05 |
| 브랜치 | spec |
| 상태 | Complete — 페르소나 B |
| 연계 | [`docs/PRD.md`](../docs/PRD.md) v0.2, [`docs/UnitConverter_MomTest_Report.md`](../docs/UnitConverter_MomTest_Report.md) |

---

## 1. Executive Summary

2026-06-05 Mom Test(페르소나 B) 결과, **단위 오타(`meters`)로 Unknown unit → ~5분 재작업**과 **전체 3단위 출력 불필요(목표 단위 선택 필요)** 가 확인되었다. PRD v0.2에 F4~F7, AC7~AC10이 반영되었고 `.cursorrules`에 SSOT로 기록되었다.

---

## 2. Mom Test 설계

### 2.1 원칙

| 원칙 | 적용 |
|------|------|
| 아이디어 말하지 않기 | OCP/CLI 솔루션 선제 제시 없음 |
| 과거·구체적 사실 | "마지막 변환 때" 질문 |
| 칭찬·미래 의견 무시 | "몇 분 걸렸나" 중심 |

### 2.2 대상

- **페르소나 B** — 단위 변환 직접 사용자
- **방식** — 5문항 순차 질의 (채팅)

---

## 3. Evidence (S1~S9)

| ID | 사실 | 영향 |
|----|------|------|
| S1 | 2026-06-05, meter→yard, 해외 메일 | 실무 맥락 |
| S2 | UnitConverter.py 사용 시도 | CLI 검증 |
| S3 | 단위명 직접 타이핑 | F4 |
| S4 | `meters` → Unknown unit | AC7, CS10 |
| S5 | 출력 후 오류 인지 | UX 지연 |
| S6 | **~5분** 재작업 | Problem Statement |
| S7 | 전체 출력 불필요 | F5, AC8 |
| S8 | **자주** 발생 | v0.2 P0 |
| S9 | 프로그램 출력 신뢰 | D5, AC10 |

---

## 4. Problem Statement (검증됨)

> 실무에서 특정 단위 쌍(meter→yard)만 필요할 때, 단위명 오타는 Unknown unit으로 실패하고 출력 확인 후 ~5분을 다시 쓴다. 세 단위 전체 출력은 불필요하며 목표 단위 선택이 필요하다.

---

## 5. PRD·규칙 반영

| 산출물 | 변경 |
|--------|------|
| `docs/PRD.md` | v0.2 — F4~F7, AC7~AC10, §2.1 Mom Test |
| `.cursorrules` | UnitConverter SSOT, v0.2 우선순위 |
| `docs/UnitConverter_MomTest_Report.md` | Q&A 전문 |

### v0.2 In Scope

| ID | 요구사항 | P |
|----|----------|---|
| F4 | 별칭·정규화 (`meters`→`meter`) | P0 |
| F5 | 목표 단위 선택 (`meter:2.5:yard`) | P0 |
| F6 | Unknown unit 제안 | P1 |
| F7 | 지원 단위 목록 | P1 |

---

## 6. Test Loop (Red 우선)

| ID | Red 시나리오 | Green 목표 |
|----|--------------|------------|
| T1 | `meters:2.5` → Unknown | 별칭 성공 |
| T2 | `meter:2.5:yard` | yard 1줄 |
| T4 | 오타 후 5분 — | 즉시 복구 |

---

## 7. 리스크·후속

| 항목 | 완화 |
|------|------|
| 단일 인터뷰 (B 1회) | 페르소나 A·C 추가 |
| "자주" 정량 없음 | AC8 TC·사용 로그 |

---

## 8. 참고

- 문제 정의: [`01_UnitConverter_ProblemDefinition_Report.md`](./01_UnitConverter_ProblemDefinition_Report.md)
- PRD: [`docs/PRD.md`](../docs/PRD.md)
- Transcript: [`Prompts/01_UnitConverter_Spec-Export-Transcript.md`](../Prompts/01_UnitConverter_Spec-Export-Transcript.md)
