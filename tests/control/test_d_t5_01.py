import pytest


def test_d_t5_01_app_modules_have_no_io_builtins(g_app_module_names: list[str]) -> None:
    # Given: app layer modules input_parser, output_formatter (AC11, A2)
    # When: AST scan for print, input, tkinter references 예정
    # Then: I/O builtins 0건 (T5, I4)
    pytest.fail("RED: D-T5-01 — app I/O static check 미구현, 의도적 실패")
