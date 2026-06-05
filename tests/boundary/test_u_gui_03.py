import pytest


def test_u_gui_03_shows_target_unit_one_line(qapp, g_to_yard: str) -> None:
    # Given: from=meter, value=2.5, to=yard (G_to_yard, Mom Test S7·S8)
    # When: Convert 클릭 후 결과 영역 검사 예정
    # Then: yard 1줄만 표시; feet/meter 3줄 없음 (G2, AC8)
    pytest.fail("RED: U-GUI-03 — 목표 단위 1줄 출력 미구현, 의도적 실패")
