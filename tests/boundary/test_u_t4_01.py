import pytest


def test_u_t4_01_unknown_with_suggestion(g_unknown_abc: str) -> None:
    # Given: CLI 입력 "abc:1" (Mom Test S6 — 5분 재작업 전 복구)
    # When: run_session(read_line=…, write=…) 호출 예정
    # Then: 지원 목록 + 제안; Unknown unit 단독 출력 금지
    pytest.fail("RED: U-T4-01 — CLI 오류 목록·제안 미구현, 의도적 실패")
