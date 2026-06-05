import importlib

from tests.ast_helpers import find_io_violations, module_qualname, module_source


def test_u_gui_01_entry_point_importable() -> None:
    # Given: GUI boundary 미구현 (PRD G5, A5 — PyQt6 진입점 분리)
    # When: gui_boundary import 및 main()/UnitConverterWindow 존재 확인
    gui_boundary = importlib.import_module("unit_converter.gui_boundary")
    gui_entry = importlib.import_module("unit_converter.gui")
    # Then: python -m unit_converter.gui 진입 가능; app/domain에 PyQt6 없음 (AC11)
    assert hasattr(gui_boundary, "UnitConverterWindow")
    assert hasattr(gui_boundary, "main")
    assert hasattr(gui_entry, "main")
    for layer, names in (("app", ["input_parser", "output_formatter"]), ("domain", ["converter", "unit_registry"])):
        for name in names:
            violations = find_io_violations(
                module_source(layer, name),
                module_label=module_qualname(layer, name),
            )
            assert violations == [], f"{layer}/{name} PyQt6/io violations: {violations}"
