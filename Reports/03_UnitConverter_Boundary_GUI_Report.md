# 03. UnitConverter Boundary·GUI Spec 보강 보고서

| 항목 | 내용 |
|------|------|
| 제품 | UnitConverter — 길이 단위 변환 (CLI + GUI) |
| 작성일 | 2026-06-05 |
| 브랜치 | spec |
| 상태 | Complete — PRD·cursorrules·README 반영 |
| 연계 | [`docs/PRD.md`](../docs/PRD.md), [`.cursorrules`](../.cursorrules) |

---

## 1. 작업 개요

| 항목 | 내용 |
|------|------|
| **목적** | GUI 도입 전 Boundary 요구사항 점검 → PRD 보강 → GUI v0.2 앞당기기 |
| **입력** | 기존 PRD v0.2 (Mom Test), `.cursorrules` 아키텍처 정의, Mom Test 증거 S1~S9 |
| **산출물** | PRD v0.2 (Boundary + GUI), `.cursorrules` 동기화, `README.md` 갱신, 본 보고서, Transcript 02 |

---

## 2. 배경 — Boundary 갭 분석

### 2.1 초기 상태

| 문서 | Boundary/GUI 반영 |
|------|-------------------|
| `.cursorrules` | ✅ boundary → control → entity 정의 |
| `docs/PRD.md` (v0.2 초안) | ⚠️ v0.3 Presenter 분리만, Boundary 용어 없음 |
| `README.md` | ❌ CLI만, GUI·Boundary 없음 |

### 2.2 1차 보강 (Boundary·GUI 요구사항 추가)

PRD에 다음을 추가했다.

- **§5.6** A1~A5 — Boundary / Control / Entity
- **§5.7** G1~G5 — GUI Boundary
- **§6** AC11, AC12 — 아키텍처·CLI/GUI 결과 일치
- **§11** v0.5 GUI 로드맵 (당시)

이때 GUI는 **v0.5**, 즉시 작업은 **CLI F4~F7 (v0.2)** 로 정리되었다.

---

## 3. Mom Test vs GUI — 문제 해소 관계

페르소나 B 인터뷰 증거와 GUI 대응:

| 증거 | 사실 | GUI (G1~G2) | CLI (F4~F7) |
|------|------|-------------|-------------|
| S3·S4 | 단위 타이핑, `meters` 오타 | 드롭다운 → 오타 거의 없음 | 별칭·제안 (F4, F6) |
| S5·S6 | 출력 후 인지, ~5분 재작업 | 선택 UI로 흐름 단축 | 즉시 피드백 (F7) |
| S7·S8 | 3단위 불필요, 목표 1줄 | G2 목표 1줄 | F5 `from:value:to` |
| S9 | 출력 신뢰 | 변환 로직 동일 (G4) | AC10 소수 정책 |

**결론:** Mom Test UX 고충(S3~S8)은 GUI가 **더 직접적**으로 해소한다. S9(정확도)는 GUI만으로는 부족 — control/entity 품질 필요.

---

## 4. 2차 보강 — GUI v0.2 앞당기기

### 4.1 의사결정

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| GUI 로드맵 | v0.5 (v0.3 Boundary 선행) | **v0.2** |
| F4~F7 우선순위 | F4·F5 P0, F6·F7 P1 | **F4~F7 전부 P0** |
| A1~A5 | v0.3 | **v0.2 최소 분리** (GUI 선행 조건) |
| v0.5 단계 | GUI boundary | **삭제** (v0.2에 통합) |

### 4.2 v0.2 통합 범위 (확정)

```
v0.2 = Mom Test (F4~F7, P0) + GUI (G1~G5) + A1~A5 최소 분리 + T1~T6, AC7~AC12
v0.3 = OCP registry 전면, AC11 정적 검사 강화
```

### 4.3 F4~F7 P0 유지 이유

GUI가 Mom Test를 주로 해소하더라도:

- CLI 실습·과제(페르소나 A) 요구
- pytest·AC7~AC10 검증 경로
- 스크립트·파이프 등 비-GUI 사용

→ **CLI 보완(F4~F7)과 GUI(G1~G2) 병행**, 둘 다 P0.

---

## 5. PRD·cursorrules 변경 요약

### 5.1 PRD (`docs/PRD.md`)

| 섹션 | 변경 |
|------|------|
| §1, §2.2~2.5 | CLI+GUI 목표, v0.2 In Scope 통합 |
| §2.3 | 웹만 비목표, 데스크톱 GUI는 v0.2 |
| §5.2 | F6, F7 → P0 |
| §5.6 | A1~A5 → v0.2 |
| §5.7 | G1~G5 → v0.2, G5 → P0 |
| §8, §10, §11 | 로드맵·리스크·갭 갱신 |

### 5.2 `.cursorrules`

- v0.2 우선순위: A1~A5 → F4~F7 → G1~G2 → G4~G5 → G3
- GUI **v0.2 P0**, AC12 Red→Green 추가

### 5.3 `README.md`

- v0.2 Spec, Mom Test, 아키텍처, GUI 실행 안내, 문서 링크 반영

---

## 6. 구현 권장 순서 (v0.2)

```
1. A1~A5 최소 분리 (entity / control / cli_boundary / gui_boundary)
2. F4~F7 — CLI Mom Test (pytest T1~T4, AC7~AC10)
3. G1, G2, G4, G5 — GUI (pytest T6, AC12)
4. G3 — 인라인 오류 (P1)
```

---

## 7. 리스크

| 항목 | 완화 |
|------|------|
| Boundary 미분리 시 Tkinter가 main에 결합 | A1~A5를 GUI 착수 전 필수 |
| CLI·GUI 결과 불일치 | 공유 control/presenter, AC12 |
| F4~F7 vs GUI 기능 중복 | 역할 분리: GUI=주 UX, CLI=TC·학습·스크립트 |

---

## 8. 참고

- PRD: [`docs/PRD.md`](../docs/PRD.md)
- Mom Test: [`docs/UnitConverter_MomTest_Report.md`](../docs/UnitConverter_MomTest_Report.md)
- Transcript: [`Prompts/02_UnitConverter_Boundary-GUI-Spec-Transcript.md`](../Prompts/02_UnitConverter_Boundary-GUI-Spec-Transcript.md)
- 이전 Transcript: [`Prompts/01_UnitConverter_Spec-Export-Transcript.md`](../Prompts/01_UnitConverter_Spec-Export-Transcript.md)
