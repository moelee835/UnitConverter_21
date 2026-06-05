from unit_converter.gui_boundary import UnitConverterWindow


def test_u_gui_04_inline_error_feedback(qapp, g_unknown_abc: str) -> None:
    # Given: 잘못된 단위 "abc" (G_unknown_abc, PRD G3, F7 — P1)
    # When: GUI Convert 클릭 후 인라인 오류 영역 검사
    window = UnitConverterWindow()
    window.apply_input(g_unknown_abc)
    error_text = window.error_label.text()
    # Then: 위젯 내 오류·지원 단위 표시; 별도 Unknown-only 금지
    assert error_text.strip() != "Unknown unit: abc"
    assert "meter" in error_text
    assert "feet" in error_text
    assert "yard" in error_text
    assert "Supported units:" in error_text
