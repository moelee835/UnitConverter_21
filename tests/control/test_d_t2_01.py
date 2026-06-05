import pytest


def test_d_t2_01_yard_one_line_only(g_to_yard: str) -> None:
    # Given: parsed meter 2.5, to_unit=yard (G_to_yard, PRD F5, AC8)
    # When: format_single_line(..., "yard") 호출 예정
    # Then: yard 1줄만; feet/meter 줄 없음 (Mom Test S7·S8)
    pytest.fail("RED: D-T2-01 — format_single_line yard 1줄 미구현, 의도적 실패")
