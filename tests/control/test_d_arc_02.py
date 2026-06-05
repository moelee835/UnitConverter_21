import pytest


def test_d_arc_02_app_does_not_import_cli(g_app_module_names: list[str]) -> None:
    # Given: app layer modules input_parser, output_formatter (A4)
    # When: AST import scan for unit_converter.cli 예정
    # Then: app → cli import 0건
    pytest.fail("RED: D-ARC-02 — app must not import cli, check 미구현, 의도적 실패")
