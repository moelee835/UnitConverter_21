import pytest


def test_d_arc_01_domain_does_not_import_app_or_cli(g_domain_module_names: list[str]) -> None:
    # Given: domain modules converter, unit_registry (A4)
    # When: AST import scan for unit_converter.app, unit_converter.cli 예정
    # Then: reverse dependency import 0건
    pytest.fail("RED: D-ARC-01 — domain reverse-import check 미구현, 의도적 실패")
