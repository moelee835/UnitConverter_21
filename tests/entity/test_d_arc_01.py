from tests.ast_helpers import find_import_violations, module_qualname, module_source

_FORBIDDEN_DOMAIN_IMPORTS = frozenset({"unit_converter.app", "unit_converter.cli"})


def test_d_arc_01_domain_does_not_import_app_or_cli(g_domain_module_names: list[str]) -> None:
    # Given: domain modules converter, unit_registry (A4)
    # When: AST import scan for unit_converter.app, unit_converter.cli
    violations: list[str] = []
    for name in g_domain_module_names:
        label = module_qualname("domain", name)
        violations.extend(
            find_import_violations(
                module_source("domain", name),
                module_label=label,
                forbidden_modules=_FORBIDDEN_DOMAIN_IMPORTS,
            )
        )
    # Then: reverse dependency import 0건
    assert violations == [], f"domain reverse-import violations: {violations}"
