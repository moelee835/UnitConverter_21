import pytest


def test_d_arc_03_gui_does_not_import_domain_converter() -> None:
    # Given: gui_boundary.py (PRD A4, A5 — app 경유)
    # When: AST import scan for unit_converter.domain.converter 직접 import
    # Then: domain.converter 직접 import 0건
    pytest.fail("RED: D-ARC-03 — gui_boundary 미구현, 의도적 실패")
