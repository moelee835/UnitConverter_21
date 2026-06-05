"""Output formatting (PRD presenter) — O3 table lines; json|csv|table v1.0."""

import csv
import io
import json

from unit_converter.domain.converter import ConversionResult
from unit_converter.domain.unit_registry import default_registry

DISPLAY_PRECISION = 6

MSG_UNKNOWN_UNIT = "Unknown unit: {unit}"
MSG_SUPPORTED_UNITS = "Supported units: {supported}"
MSG_DID_YOU_MEAN = "Did you mean {suggestion}?"


def format_value(value: float) -> str:
    """AC10 / CS13 — consistent decimal display; strip float noise."""
    rounded = round(value, DISPLAY_PRECISION)
    return f"{rounded:.{DISPLAY_PRECISION}f}".rstrip("0").rstrip(".")


def format_line(source_value: float, source_unit: str, converted: float, target_unit: str) -> str:
    return f"{format_value(source_value)} {source_unit} = {format_value(converted)} {target_unit}"


def _target_pairs(result: ConversionResult, target_unit: str | None) -> list[tuple[str, float]]:
    if target_unit is not None:
        converted = result.targets.get(target_unit)
        if converted is None:
            return []
        return [(target_unit, converted)]
    return sorted(result.targets.items())


def _numeric(value: float) -> float:
    return round(value, DISPLAY_PRECISION)


def format_result_json(result: ConversionResult, target_unit: str | None = None) -> str:
    """PRD v1.0 — JSON presenter."""
    payload = {
        "source": {"unit": result.source_unit, "value": _numeric(result.source_value)},
        "conversions": [
            {"unit": unit, "value": _numeric(converted)}
            for unit, converted in _target_pairs(result, target_unit)
        ],
    }
    return json.dumps(payload, separators=(",", ":"))


def format_result_csv_lines(result: ConversionResult, target_unit: str | None = None) -> list[str]:
    """PRD v1.0 — CSV presenter (header + rows)."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["from_unit", "from_value", "to_unit", "to_value"])
    for unit, converted in _target_pairs(result, target_unit):
        writer.writerow(
            [
                result.source_unit,
                format_value(result.source_value),
                unit,
                format_value(converted),
            ]
        )
    return buffer.getvalue().splitlines()


def format_result_lines(
    result: ConversionResult,
    target_unit: str | None,
    output_format: str,
) -> list[str]:
    """Route to table / json / csv presenter (Strategy)."""
    if output_format == "json":
        return [format_result_json(result, target_unit)]
    if output_format == "csv":
        return format_result_csv_lines(result, target_unit)
    if target_unit:
        line = format_single_line(result, target_unit)
        return [line] if line is not None else []
    return format_all_lines(result)


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


def format_unknown_unit_message(unit: str) -> str:
    """Unknown unit error with supported list and optional suggestion (PRD F6, F7)."""
    from unit_converter.app.input_parser import suggest_unit

    reg = default_registry()
    supported = ", ".join(reg.names())
    lines = [
        MSG_UNKNOWN_UNIT.format(unit=unit),
        MSG_SUPPORTED_UNITS.format(supported=supported),
    ]
    suggestion = suggest_unit(unit)
    if suggestion:
        lines.append(MSG_DID_YOU_MEAN.format(suggestion=suggestion))
    return "\n".join(lines)
