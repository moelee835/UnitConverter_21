from tests.ast_helpers import find_io_violations, module_qualname, module_source


def test_d_t5_01_app_modules_have_no_io_builtins(g_app_module_names: list[str]) -> None:
    # Given: app layer modules input_parser, output_formatter (AC11, A2)
    # When: AST scan for print, input, tkinter references
    violations: list[str] = []
    for name in g_app_module_names:
        label = module_qualname("app", name)
        violations.extend(find_io_violations(module_source("app", name), module_label=label))
    # Then: I/O builtins 0건 (T5, I4)
    assert violations == [], f"app I/O violations: {violations}"
