"""Output formatting (PRD presenter) — O3 table lines; json|csv in v1.0."""

from unit_converter.domain.converter import ConversionResult


def format_line(source_value: float, source_unit: str, converted: float, target_unit: str) -> str:
    return f"{source_value} {source_unit} = {converted} {target_unit}"


def format_all_lines(result: ConversionResult) -> list[str]:
    """PRD O1 / AC1: all registered units (v0.2 Phase 0 default)."""
    lines: list[str] = []
    for target_unit, converted in sorted(result.targets.items()):
        lines.append(
            format_line(result.source_value, result.source_unit, converted, target_unit)
        )
    return lines


def format_single_line(
    result: ConversionResult,
    target_unit: str,
) -> str | None:
    """PRD O2 / AC8 — Phase 2."""
    converted = result.targets.get(target_unit)
    if converted is None:
        return None
    return format_line(result.source_value, result.source_unit, converted, target_unit)
