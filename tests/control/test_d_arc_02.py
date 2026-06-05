from tests.ast_helpers import find_import_violations, module_qualname, module_source

_FORBIDDEN_APP_CLI_IMPORTS = frozenset({"unit_converter.cli"})


def test_d_arc_02_app_does_not_import_cli(g_app_module_names: list[str]) -> None:
    # Given: app layer modules input_parser, output_formatter (A4)
    # When: AST import scan for unit_converter.cli
    violations: list[str] = []
    for name in g_app_module_names:
        label = module_qualname("app", name)
        violations.extend(
            find_import_violations(
                module_source("app", name),
                module_label=label,
                forbidden_modules=_FORBIDDEN_APP_CLI_IMPORTS,
            )
        )
    # Then: app → cli import 0건
    assert violations == [], f"app→cli import violations: {violations}"
