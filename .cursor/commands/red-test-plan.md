# /red-test-plan — ARRR Ask · RED 설계 (C2C)

UnitConverter Dual Track **Discovery(Ask)** — ①기획 → ②설계 → ③RED 설계.  
`.cursorrules`, `.cursor/skills/red-test-plan/SKILL.md`, `docs/PRD.md` 와 함께 적용.

**이 Command는 파일을 만들지 않는다.** `tests/`, `src/`, `parser.py` 등 생성·수정 금지.

---

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: entity|control|boundary | Track: Logic|UI
이번 RED 묶음: <Test ID> (<PRD ID>, Tn, AC>)
```

사용자가 Layer·Track·Test ID를 생략하면 Phase 0·Logic·`D-T5-01` 후보를 제안하고 확인한다.

---

## C2C 규칙

| Rule | 내용 |
|------|------|
| **1** | 판단 포함 항목만 To-Do (“허용한다/금지한다”) — 단순 행동 to-do 폐기 |
| **2** | 1 To-Do : 1 Test Case — 복합 항목은 분해 |
| **3** | RED 먼저 — 모든 케이스 FAIL/ERROR 전제, 구현은 나중 |

---

## RED 단계 절대 금지

- 구현 코드 작성 / GREEN·REFACTOR 진입
- 모든 테스트는 현재 **실패(FAIL/ERROR)** 상태로만 기술
- 의도적 RED: `pytest.fail("RED: [Test ID]")` 한 줄로만 표기
- **Logic Track:** Domain(registry·converter) Mock 금지 · 픽스처만
- **UI Track:** control Mock 허용
- skip / xfail / assert 완화 금지

---

## 절차

1. **① 기획** — `docs/PRD.md`에서 요구 ID 인용 (F*, I*, AC*, T1~T6). Mom Test Evidence(S*) 연결.
2. **② 설계** — Layer·Track·대상 함수(`parser` 등). `.cursor/skills/red-test-plan/reference.md` ID 규칙.
3. **③ RED 설계** — 아래 **두 표 형식** 우선 (해당 Track만이면 하나).
4. **4섹션 출력** — C2C · RED 표 · 테스트 플랜 · ECB·Mock 점검.
5. **완료 한 줄** — `RED 설계 완료 — /red-skeleton 으로 테스트 골격 생성 가능.`

---

## RED 설계표 형식 (필수)

### UI/Boundary (Track UI, `U-*`)

| Test ID | Given | Then (기대값) | Expected RED Failure |
|---------|-------|---------------|----------------------|
| U-… | … | … | ModuleNotFoundError / AssertionError / pytest.fail RED |

### Domain/Logic (Track Logic, `D-*`)

| Test ID | 대상 함수 | Given→Then | Invariant | Expected RED Failure |
|---------|-----------|------------|-----------|----------------------|
| D-… | … | … | I1~I5 (reference.md) | … |

---

## 출력 섹션 (순서 고정)

### 1. C2C 추적 (Rule 1~3)

- **PRD 인용** — `docs/PRD.md` 해당 절·ID (예: F4, I6, AC7, T1)
- **To-Do 1개** — 판단 문장만
- **Test ID** → Given / When / Then

### 2. Track RED 설계표

- Logic → `D-*` 표
- UI → `U-*` 표 (boundary·CLI/GUI)

### 3. 테스트 플랜 (파일 생성 없음 — 경로만)

- 파일: 예 `tests/control/test_d_t1_01.py`
- `test_*` 함수명 후보
- conftest 픽스처: `G_meter_2_5`, `G_meters_typo` 등 (**로직 데이터만**, Mock 아님)
- pytest 명령 예:

```bash
python -m pytest tests/control/test_d_t1_01.py::test_d_t1_01_meters_alias_to_meter -v
```

- RED 묶음 범위 (이번 1~3 ID)

### 4. ECB·Mock 점검

- Logic Track → registry/converter **Mock 금지**
- boundary → 사용자 메시지·I/O; control → `input`/`print`/tkinter 없음 (T5/AC11)
- v0.2: `boundary → control → entity`, 역방향 import 금지

---

## 호출 예시 (사용자 메시지)

```
/red-test-plan
Phase: red | Layer: control | Track: Logic
이번 RED 묶음: D-T1-01 (F4, T1, AC7)
다음을 표로 작성해줘. tests/·src/ 파일은 만들지 마.
1. C2C 추적 (Rule 1~3)
2. Track B (D-*) RED 설계표
3. 테스트 플랜
4. ECB·Mock 점검
금지: src/·tests/ 수정, GREEN/REFACTOR, skip/xfail
완료 후: /red-skeleton 으로 넘길 준비됐다고 한 줄로 알려줘.
```

---

## 금지

| 금지 | |
|------|--|
| `tests/`, `src/`, `*.py` 생성·수정 | |
| GREEN / REFACTOR | |
| Logic Track Domain Mock | |
| skip / xfail / assert 완화 | |
| PRD v0.2 밖 일괄 설계 | 로드맵 §11 안내 |

---

## 다음 Command

| Command | 역할 |
|---------|------|
| [`/red-skeleton`](../commands/red-skeleton.md) | 설계표 기준 `tests/` 골격·`pytest.fail` RED |
| [`/green-minimal`](../commands/green-minimal.md) | 최소 구현 GREEN |
