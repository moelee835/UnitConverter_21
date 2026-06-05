# /green-minimal — ARRR Respond · 최소 GREEN

UnitConverter Dual Track **Respond(Delivery)** — RED로 확정된 **Test ID 1개**만 최소 구현으로 통과.  
`.cursorrules`, `.cursor/skills/green-minimal/SKILL.md`, `/red-skeleton` 산출물과 함께 적용.

**git commit:** 사용자가 요청할 때만.

---

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity|control|boundary | Track: Logic|UI
RED 대상: <Test ID> (<tests/.../test_*.py>)
```

---

## 절차

### 1. RED 재확인

의도적 `pytest.fail` / FAIL 상태인지 실행:

```bash
python -m pytest <tests/.../test_*.py>::<test_function> -v
```

이미 PASSED면 중단·원인 보고.

### 2. 최소 구현

대상 Layer에 **이번 Test ID를 통과시키는 최소 코드만** 추가.

| Layer | 경로 (루트 패키지, `src/` 없음) |
|-------|--------------------------------|
| entity | `entity/constants.py`, `entity/unit_registry.py` |
| control | `control/parser.py`, `control/converter.py`, `control/presenter.py` |
| boundary | `boundary/cli_boundary.py`, `boundary/gui_boundary.py` |

**원칙**

- 하드코딩·매직넘버 금지 → `entity/constants.py` SSOT (`3.28084`, `1.09361`)
- ECB: `boundary → control → entity`; **역방향 import 금지**
- entity·control: `input` / `print` / GUI 프레임워크(`tkinter`, `PyQt6`) **금지** (AC11); PyQt6는 `gui_boundary`만
- entity에 boundary 스타일 오류 처리·사용자 메시지 로직 **금지** (E001~E007 해당 패턴 금지와 동일)

### 3. 스켈레톤 → assert

- `pytest.fail("RED: …")` 제거
- When: 실제 함수 호출
- Then: 설계표 기대값 `assert`

### 4. PASS 확인

```bash
python -m pytest <tests/.../test_*.py>::<test_function> -v
python -m pytest <tests/.../test_*.py> -v
```

### 5. (선택) REPL 스모크

Given·Then을 REPL 1~2줄로 검증 (예: `normalize_unit("meters") == "meter"`).

---

## 호출 예시 (사용자 메시지)

```
/green-minimal
Phase: green | Layer: control | Track: Logic
RED 대상: D-T1-01 (tests/control/test_d_t1_01.py)
1. RED 재확인 — pytest.fail 상태인지 pytest 실행
2. control/parser.py 에 normalize_unit() 최소 구현
   - 매직넘버 금지 → entity/constants.py SSOT (필요 시)
   - entity·control: input/print/GUI 프레임워크(tkinter, PyQt6) 금지
   - ECB: entity는 boundary/control import 금지
3. RED 스켈레톤의 pytest.fail 제거 → 실제 assert로 교체
4. PASS 확인:
   python -m pytest tests/control/test_d_t1_01.py::test_d_t1_01_meters_alias_to_meter -v
   python -m pytest tests/control/test_d_t1_01.py -v
5. (선택) REPL — normalize_unit("meters") == "meter"
금지: 이번 RED 묶음 외 ID 동시 해결, REFACTOR, assert 완화
보고: PASS Test ID · 변경 파일 · 회귀 실패 시 즉시 수정
git commit은 내가 요청할 때만.
```

---

## Logic 예시 (D-T1-01)

**구현:** `control/parser.py`

```python
def normalize_unit(raw: str) -> str:
    aliases = {"meters": "meter"}
    u = raw.strip().lower()
    return aliases.get(u, u)  # 최소: meters→meter; GREEN 범위만
```

**테스트 Then:**

```python
assert normalize_unit("meters") == "meter"
```

---

## GREEN 보고 형식

```markdown
## GREEN Minimal 보고

- **Test ID:** D-T1-01 — PASSED
- **pytest:** (단일) passed · (파일) N passed
- **변경 파일:** tests/..., control/parser.py, ...
- **회귀:** 없음
```

완료 한 줄: `GREEN 완료 — <Test ID> PASSED.`

---

## 금지

| 금지 | |
|------|--|
| 이번 RED 묶음 외 ID | |
| REFACTOR | |
| assert 완화 · skip · xfail | |
| git commit (명시 요청 전) | |
| RED 없는 기능 일괄 구현 | |

---

## ARRR Command 체인

| # | Command |
|---|---------|
| 1 | `/red-test-plan` |
| 2 | `/red-skeleton` |
| 3 | **`/green-minimal`** |
| 4 | [`/golden-master`](../commands/golden-master.md) (PASS 후) |
| 5 | REFACTOR (예정) |
