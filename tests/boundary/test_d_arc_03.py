from pathlib import Path

from tests.ast_helpers import find_import_violations

_FORBIDDEN_GUI_IMPORTS = frozenset({"unit_converter.domain.converter"})


def test_d_arc_03_gui_does_not_import_domain_converter() -> None:
    # Given: gui_boundary.py (PRD A4, A5 — app 경유)
    # When: AST import scan for unit_converter.domain.converter 직접 import
    source = (
        Path(__file__).resolve().parent.parent.parent
        / "unit_converter"
        / "gui_boundary.py"
    ).read_text(encoding="utf-8")
    violations = find_import_violations(
        source,
        module_label="unit_converter.gui_boundary",
        forbidden_modules=_FORBIDDEN_GUI_IMPORTS,
    )
    # Then: domain.converter 직접 import 0건
    assert violations == [], f"gui→domain.converter import violations: {violations}"
