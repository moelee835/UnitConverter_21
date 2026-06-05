"""AST static checks for Phase 0 architecture guard tests (D-T5-01, D-ARC-01, D-ARC-02)."""

from __future__ import annotations

import ast
from pathlib import Path

_PACKAGE_ROOT = Path(__file__).resolve().parent.parent / "unit_converter"

_IO_FORBIDDEN_NAMES = frozenset({"print", "input"})
_IO_FORBIDDEN_MODULE_ROOTS = frozenset({"tkinter", "PyQt6"})


def module_source(layer: str, module_name: str) -> str:
    path = _PACKAGE_ROOT / layer / f"{module_name}.py"
    return path.read_text(encoding="utf-8")


def module_qualname(layer: str, module_name: str) -> str:
    return f"unit_converter.{layer}.{module_name}"


def find_io_violations(source: str, *, module_label: str) -> list[str]:
    """Detect print/input names or calls and tkinter/PyQt6 imports in app/domain code."""
    tree = ast.parse(source, filename=module_label)
    violations: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in _IO_FORBIDDEN_NAMES:
            violations.append(f"{module_label}:{node.lineno}: name '{node.id}'")

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in _IO_FORBIDDEN_NAMES:
                violations.append(f"{module_label}:{node.lineno}: call '{node.func.id}()'")

        if isinstance(node, ast.Import):
            for alias in node.names:
                if _is_forbidden_io_module(alias.name):
                    violations.append(
                        f"{module_label}:{node.lineno}: import '{alias.name}'"
                    )

        if isinstance(node, ast.ImportFrom):
            for absolute in _resolve_import_from(module_label, node):
                if _is_forbidden_io_module(absolute):
                    violations.append(
                        f"{module_label}:{node.lineno}: import from '{absolute}'"
                    )

    return violations


def find_import_violations(
    source: str,
    *,
    module_label: str,
    forbidden_modules: frozenset[str],
) -> list[str]:
    """Detect imports whose absolute module name matches forbidden prefixes."""
    tree = ast.parse(source, filename=module_label)
    violations: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _matches_forbidden_module(alias.name, forbidden_modules):
                    violations.append(
                        f"{module_label}:{node.lineno}: import '{alias.name}'"
                    )

        if isinstance(node, ast.ImportFrom):
            for absolute in _resolve_import_from(module_label, node):
                if _matches_forbidden_module(absolute, forbidden_modules):
                    imported = node.module or "."
                    violations.append(
                        f"{module_label}:{node.lineno}: import from '{imported}'"
                    )

    return violations


def _is_forbidden_io_module(module: str) -> bool:
    root = module.split(".")[0]
    return root in _IO_FORBIDDEN_MODULE_ROOTS


def _matches_forbidden_module(module: str, forbidden_modules: frozenset[str]) -> bool:
    return any(
        module == forbidden or module.startswith(f"{forbidden}.")
        for forbidden in forbidden_modules
    )


def _resolve_import_from(current_module: str, node: ast.ImportFrom) -> list[str]:
    parts = current_module.split(".")
    if node.level > 0:
        base = parts[: max(len(parts) - node.level, 0)]
        if node.module:
            return [".".join(base + node.module.split("."))]
        return [".".join(base)] if base else []
    if node.module:
        return [node.module]
    return []
