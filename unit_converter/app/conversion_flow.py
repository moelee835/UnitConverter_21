"""Shared conversion orchestration (PRD G4, T6) — CLI·GUI common path."""

from unit_converter.app.input_parser import ParsedInput
from unit_converter.app.output_formatter import (
    format_result_lines,
    format_unknown_unit_message,
)
from unit_converter.domain.converter import convert
from unit_converter.domain.unit_registry import UnitRegistry, default_registry


def convert_parsed(
    parsed: ParsedInput,
    registry: UnitRegistry | None = None,
) -> list[str]:
    """Parse → convert → format; raises ValueError with F6/F7 message on unknown unit."""
    reg = registry or default_registry()
    if reg.get(parsed.unit) is None:
        raise ValueError(format_unknown_unit_message(parsed.unit))
    if parsed.to_unit is not None and reg.get(parsed.to_unit) is None:
        raise ValueError(format_unknown_unit_message(parsed.to_unit))

    result = convert(parsed.unit, parsed.value, reg)
    lines = format_result_lines(result, parsed.to_unit, parsed.output_format)
    if parsed.to_unit and not lines and parsed.output_format == "table":
        raise ValueError(format_unknown_unit_message(parsed.to_unit))
    return lines
