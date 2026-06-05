from unit_converter.gui_boundary import UnitConverterWindow


def test_u_gui_02_from_to_unit_dropdowns(qapp) -> None:
    # Given: GUI 창 (headless QApplication, Mom Test S3·S4)
    # When: UnitConverterWindow 표시 후 from/to 단위 선택 위젯 검사
    window = UnitConverterWindow()
    # Then: from·to registry SSOT 단위 선택 UI (G1 — cubit 포함)
    for combo in (window.from_unit, window.to_unit):
        assert combo.count() == 4
        for unit in ("cubit", "meter", "feet", "yard"):
            assert combo.findText(unit) >= 0
