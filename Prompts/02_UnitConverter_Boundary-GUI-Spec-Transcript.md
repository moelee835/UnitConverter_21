# 02. UnitConverter Boundary·GUI Spec — Prompt Export Transcript

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_21 |
| 브랜치 | spec |
| 작성일 | 2026-06-05 |
| 세션 | spec — Boundary 점검 · GUI Spec · v0.2 로드맵 조정 |

---

## Turn 1 — User

```
GUI도 추가하려고 하는데, Boundary 관련된 요구사항이 PRD.md 등에 반영되어 있는지 체크해줘
```

## Turn 1 — Assistant (요약)

- PRD·README·Reports 검색: Boundary 용어는 **`.cursorrules`에만** 상세, PRD는 v0.3 Presenter 분리 수준
- GUI는 §2.3 **비목표**, 로드맵·AC 없음
- 갭 목록: A1~A5, G1~G5, AC11~AC12, 다중 boundary
- 권장 PRD 보강 항목 제시 (§5.6, §5.7, §11 등)

---

## Turn 2 — User

```
위 권장사항을 반영하세요
```

## Turn 2 — Assistant (요약)

- `docs/PRD.md`: §5.6 A1~A5, §5.7 G1~G5, AC11~AC12, §2.5, 로드맵 v0.5 GUI 추가
- `.cursorrules`: 아키텍처 SSOT PRD §5.6 동기화, v0.3/v0.5 우선순위

---

## Turn 3 — User

```
읽다보니까 뭔가 바로 작업될 사항들은 CLI 기준이고 GUI는 밀려난것 같은데 맞나?
```

## Turn 3 — Assistant (요약)

- **맞음** — v0.2 즉시 작업은 CLI (F4~F7), GUI는 v0.5
- Mom Test 증거는 CLI 사용에서 나옴, 페르소나 A 실습도 CLI
- GUI는 요구사항만 문서화, v0.3 Boundary 선행 후 v0.5

---

## Turn 4 — User

```
Mom Test에서 내가 말했던 사항들은 GUI 도입으로 모두 해소되는 거잖아.
```

## Turn 4 — Assistant (요약)

- **거의 맞음** — S3~S8은 GUI(G1~G2)가 더 직접 해소
- **S9(정확도)** 는 GUI만으로 부족, control 품질 필요
- PRD가 CLI v0.2 + GUI v0.5로 둔 이유: Mom Test 도구가 CLI, 학습 요구, 구현 순서

---

## Turn 5 — User

```
GUI를 구현해야하니 v0.2로 앞당겨서 구현토록 수정해
```

## Turn 5 — Assistant (요약)

- Ask 모드 — 수정 불가, Agent 모드 전환 및 F4~F7 P0 유지 여부 질문 제시

---

## Turn 6 — User

```
F4~F7는 P0 유지.
```

## Turn 6 — Assistant (요약)

- `docs/PRD.md`: GUI → v0.2, F6·F7 P0, A1~A5 v0.2 최소 분리, v0.5 삭제
- `.cursorrules`: v0.2 = A1~A5 → F4~F7 → G1~G5, AC12 추가

---

## Turn 7 — User

```
지금까지 내용을 Report/ 아래 리포트로 출력하고 Prompt Transcript도 작성해. 그리고 spec 브랜치를 푸쉬해
```

## Turn 7 — Assistant (요약)

- (중단 후 Turn 8에서 이어짐)

---

## Turn 8 — User

```
푸쉬 전에 README.md에도 반영해
```

## Turn 8 — Assistant (요약)

- `README.md` v0.2 Spec, Mom Test, 아키텍처, GUI, 문서 링크 반영
- `Reports/03_UnitConverter_Boundary_GUI_Report.md` 작성
- `Prompts/02_UnitConverter_Boundary-GUI-Spec-Transcript.md` 작성 (본 문서)
- spec 브랜치 커밋·푸시

---

## 산출물 목록

| 경로 | 설명 |
|------|------|
| `docs/PRD.md` | PRD v0.2 (Mom Test + GUI + A1~A5) |
| `.cursorrules` | v0.2 우선순위·아키텍처 |
| `README.md` | v0.2·GUI·Boundary·문서 링크 |
| `Reports/03_UnitConverter_Boundary_GUI_Report.md` | Boundary·GUI Spec 보강 보고서 |
| `Prompts/02_UnitConverter_Boundary-GUI-Spec-Transcript.md` | 본 Transcript |

---

## Evidence Quick Reference

| ID | 한 줄 요약 |
|----|-----------|
| S3·S4 | 단위 타이핑·`meters` 오타 |
| S6 | ~5분 재작업 |
| S7·S8 | 목표 단위 1줄만, 자주 |
| G1·G2 | GUI 드롭다운 + 1줄 출력 (v0.2 P0) |
| F4~F7 | CLI 보완 (v0.2 P0, TC·학습) |
