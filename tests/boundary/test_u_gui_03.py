from unit_converter.gui_boundary import UnitConverterWindow


def test_u_gui_03_shows_target_unit_one_line(qapp, g_to_yard: str) -> None:
    # Given: from=meter, value=2.5, to=yard (G_to_yard, Mom Test S7·S8)
    # When: Convert 클릭 후 결과 영역 검사
    window = UnitConverterWindow()
    window.apply_input(g_to_yard)
    result = window.get_result_text()
    # Then: yard 1줄만 표시; feet/meter 3줄 없음 (G2, AC8)
    assert result == "2.5 meter = 2.734025 yard"
    assert "feet" not in result
    assert result.count("\n") == 0
