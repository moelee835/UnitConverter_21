# /refactor-safe — ARRR Refactor · 코드 스멜 개선 (Budget 1개)

UnitConverter — `/refactor-smell` 표에서 **선택한 스멜 1개**만 Change Budget 내 리팩터.  
`.cursorrules`, `docs/Code_smell.md`, `.cursor/skills/refactor-safe/SKILL.md`.

**git commit:** 사용자 요청 시만.

---

## 필수 선언 (응답 첫 줄)

```
Phase: refactor | Scope: <paths> | Track: Logic+UI
스멜: <이름> (CSx) | Budget: 파일≤N · 클래스≤C · 메서드≤M
```

---

## 선행 조건

1. `docs/Code_smell.md` — `/refactor-smell` 완료  
2. ```bash
   python -m pytest tests/ -v
   ```
   **전부 PASS** — 아니면 **중단**  
3. 사용자 메시지에 **스멜 1개·대상·Budget** 포함

---

## Change Budget

| 항목 | 한도 |
|------|------|
| 파일 | ≤ 3 |
| 클래스 | ≤ 1 |
| 메서드 | ≤ 3 |

---

## 원칙 (동작 불변)

| 원칙 | 내용 |
|------|------|
| 입출력 | CLI/GUI **문자열·오류 메시지** 동일 (O3, AC1~AC8) |
| int[6]·E001~E005 | **미사용** — MagicSquare 계약 적용 안 함 |
| entity | 사용자 오류 **emit·print·input** 추가 금지 |
| ECB | 역방향 import 금지 |
| 테스트 | assert 완화 · skip · xfail 금지 |
| 범위 | **기능 추가·버그 수정 금지** — 별도 GREEN |

---

## 절차

1. `Code_smell.md`에서 해당 행 확인  
2. Budget 내 **extract / SSOT 상수 / 모듈 이동**만 수행  
3. 회귀:

```bash
python -m pytest tests/ -v
```

4. Golden (baseline 있을 때, `UPDATE_GOLDEN` **없음**):

```bash
python -m pytest tests/control/test_d_t2_01.py -v
# 또는 이번 스멜과 연관된 golden 테스트 경로
```

5. **golden diff**

| 유형 | 조치 |
|------|------|
| **비의도** | 리팩터 **롤백** |
| **의도** | `Reports/`·PRD 근거 + `UPDATE_GOLDEN=1` 후 재검증 |

6. 보고 (아래 형식)

---

## 호출 예시 (사용자 메시지)

```
/refactor-safe
/refactor-smell 표에서 선택한 스멜 1개만:
- 스멜: Duplicated Code (CS5, CS6) — 변환·출력 이중
- 대상: UnitConverter.py:main
- Budget: 파일 2개, 메서드 2개 extract (to_meter, from_meter)
원칙:
- 입출력·예외 메시지 변경 금지
- entity에 print/input/사용자 오류 처리 추가 금지
- assert 완화·skip 금지
- 기능 추가·버그 수정 금지 (별도 GREEN)
완료 후:
python -m pytest tests/ -v
golden matched (UPDATE_GOLDEN 없음):
python -m pytest tests/control/test_d_t2_01.py -v
golden diff:
- 의도적 → Reports/PRD 근거 + UPDATE_GOLDEN=1
- 비의도 → 롤백
보고: 변경 요약 · pytest 결과 · golden matched 여부
```

### UnitConverter 매핑 (MagicSquare 예시 대체)

| 예시 (타 프로젝트) | 본 프로젝트 |
|--------------------|-------------|
| 10선 합 4곳 반복 | `main()` 내 to_meter + `*3.28084`/`*1.09361` + print 3줄 |
| `src/entity/validation.py` | `UnitConverter.py` → `entity/constants.py` + `control/converter.py` |
| `sum_row`, `sum_col` | `to_meter`, `from_meter` (또는 `convert_to_unit`) |

---

## 보고 형식

```markdown
## Refactor Safe 보고

- **스멜:** Duplicated Code (CS6)
- **Budget 사용:** 파일 2/3 · 메서드 2/3
- **변경:** entity/constants.py (신규), control/converter.py (신규), UnitConverter.py (위임만)
- **pytest:** `tests/` — N passed, 0 failed
- **golden:** matched | N/A | 의도적 diff → UPDATE_GOLDEN=1 적용
- **롤백:** 없음 | (사유)
```

완료 한 줄: `Refactor Safe 완료 — <CSx> Budget 내, pytest PASS.`

---

## 금지

| 금지 | |
|------|--|
| 스멜 2개 이상 | |
| Budget 초과 | |
| Mom Test 신규 동작 (별칭·1줄 출력 등) 이번 턴 | |
| `Code_smell.md` 없이 대규모 리팩터 | |
| golden 수동 편집 | |
| git commit (명시 요청 전) | |

---

## ARRR Command 체인

| # | Command |
|---|---------|
| 5 | `/refactor-smell` |
| 6 | **`/refactor-safe`** (본 Command) |
