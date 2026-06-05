import pytest


def test_u_t2_01_cli_yard_only(g_to_yard: str) -> None:
    # Given: CLI 입력 "meter:2.5:yard" (AC8, T2)
    # When: run_session(read_line=…, write=…) 호출 예정
    # Then: 출력 1줄, yard만; feet/meter 3줄 없음
    pytest.fail("RED: U-T2-01 — CLI yard 1줄 출력 미구현, 의도적 실패")
