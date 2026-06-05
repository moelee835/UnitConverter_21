# 06. UnitConverter RED v0.2 전 Phase — Prompt Export Transcript

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_21 |
| 작성일 | 2026-06-05 |
| 세션 | Phase 1~5 RED 설계·스켈레톤 (CLI F4~F7 + GUI G1~G5) |

---

## Turn 1 — User

```
/red-test-plan
```

## Turn 1 — Assistant (요약)

- **선언:** Phase: red | Layer: control | Track: Logic — Phase 1 후보 D-T1-01 (F4, T1, AC7)
- Phase 0(D-T5-01, D-ARC-01, D-ARC-02) GREEN 완료(Report 06) 확인
- **C2C:** F4·I6·T1·AC7 — `normalize_unit("meters")`→`meter`; U-T1-01 CLI Unknown 금지
- RED 설계표·테스트 플랜·ECB 점검 출력 (코드 생성 없음)
- 완료: `/red-skeleton` 안내

---

## Turn 2 — User

```
GUI Boundary 까지 레드 계획에 보함하세요
```

## Turn 2 — Assistant (요약)

- v0.2 **전 Phase** RED 설계 확장 — Phase 1~5 통합 로드맵
- **Phase 5 GUI:** U-GUI-01(G5 진입점), U-GUI-02(G1 드롭다운), U-GUI-03(G2 1줄), U-T6-01(G4/AC12), D-T6-01, D-ARC-03, U-GUI-04(P1)
- Mom Test S3~S9 ↔ CLI/GUI Track 매핑
- Phase 2(D-T2-01, U-T2-01), Phase 3~4(D-T4-*, U-T4-01) 포함

---

## Turn 3 — User

```
/red-skeleton
```

## Turn 3 — Assistant (요약)

- **Phase 1 RED 스켈레톤 3건** 작성
- `tests/control/test_d_t1_01.py`, `test_d_t1_02.py`, `tests/boundary/test_u_t1_01.py`
- `conftest.py` — `g_meter_trimmed` 추가
- pytest: **3 failed** (의도적 RED)
- venv 생성·`pip install -r requirements.txt` 실행

---

## Turn 4 — User

```
/red-skeleton Phase 5 — U-GUI-01~03, U-T6-01. 미작성된 RED가 없는지 체크.
```

## Turn 4 — Assistant (요약)

- **Phase 5 UI 4건** 스켈레톤: U-GUI-01~03, U-T6-01
- `conftest.py` — `qapp` 세션 픽스처 (headless QApplication)
- pytest: **4 failed**
- **미작성 점검:** Phase 2·3~4·Phase 5 Logic(D-ARC-03, D-T6-01, U-GUI-04) **미작성** 목록 보고

---

## Turn 5 — User

```
Phase 2(D-T2-01, U-T2-01) 등 남은 페이즈도 모두 RED단계 수행
```

## Turn 5 — Assistant (요약)

- **잔여 8건** RED 스켈레톤 작성:
  - Phase 2: D-T2-01, U-T2-01
  - Phase 3~4: D-T4-01, D-T4-02, U-T4-01
  - Phase 5: D-ARC-03, D-T6-01, U-GUI-04
- `conftest.py` — `g_unknown_abc`, `g_meterss_typo` 추가
- **v0.2 RED 전체 15건** — pytest **15 failed**
- 전체 `tests/`: **15 failed, 8 passed**

---

## Turn 6 — User

```
Reports/ 보고서 생성 및 Prompts Transcript 진행. 그리고 README.md에도 반영.
```

## Turn 6 — Assistant (요약)

- `Reports/07_UnitConverter_RED_v0.2_Full-Phase_Report.md` — 본 세션 종합 보고서
- `Prompts/06_UnitConverter_RED-v0.2-Full-Phase-Transcript.md` — 본 Transcript
- `README.md` — Phase 1~5 RED 반영, 테스트·문서 링크 갱신
- `docs/PRD.md` §12 — Report 07·Prompt 06 참고 링크

---

## 산출물 목록 (본 세션 누적)

| 유형 | 경로 |
|------|------|
| RED 설계 | 대화 출력 (`/red-test-plan` ×2) |
| RED 스켈레톤 | `tests/control/test_d_t*.py` (6), `tests/boundary/test_u_*.py` (9) |
| conftest | `g_meter_trimmed`, `g_unknown_abc`, `g_meterss_typo`, `qapp` |
| 보고서 | `Reports/07_UnitConverter_RED_v0.2_Full-Phase_Report.md` |
| Transcript | `Prompts/06_UnitConverter_RED-v0.2-Full-Phase-Transcript.md` |
| README | Phase·pytest·문서 링크 갱신 |

---

## pytest 요약 (세션 종료 시점)

```bash
venv\Scripts\python.exe -m pytest tests/ -v
# 15 failed, 8 passed in ~0.2s
```

| 구분 | 건수 |
|------|------|
| 🔴 RED (의도적 fail) | 15 |
| 🟢 GREEN | 8 |

---

## 다음 Command (권장)

| 순서 | Command | 대상 |
|------|---------|------|
| 1 | `/green-minimal` | D-T1-01 — `normalize_unit` |
| 2 | `/green-minimal` | D-T1-02, U-T1-01 |
| 3 | `/golden-master` | D-T2-01 (Phase 2 후) |
| 4 | `/green-minimal` | Phase 5 — U-GUI-01 (gui_boundary 골격) |

---

## 참고 링크

- Report 07: [`Reports/07_UnitConverter_RED_v0.2_Full-Phase_Report.md`](../Reports/07_UnitConverter_RED_v0.2_Full-Phase_Report.md)
- Report 06 (선행 GREEN): [`Reports/06_UnitConverter_GREEN-Golden_Phase_Report.md`](../Reports/06_UnitConverter_GREEN-Golden_Phase_Report.md)
- RED Skill: [`.cursor/skills/red-test-plan/SKILL.md`](../.cursor/skills/red-test-plan/SKILL.md)
- Skeleton Skill: [`.cursor/skills/red-skeleton/SKILL.md`](../.cursor/skills/red-skeleton/SKILL.md)
