"""Input parsing (PRD parser) — I1, I3, I4; F4/I6 in Phase 1."""

from dataclasses import dataclass


class ParseError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class ParsedInput:
    unit: str
    value: float
    to_unit: str | None = None


def parse_input(raw: str) -> ParsedInput:
    """Parse `{from_unit}:{value}` (PRD I1). `from:value:to` — Phase 2."""
    if ":" not in raw:
        raise ParseError("Invalid format. Use unit:value (ex: meter:2.5)")

    parts = raw.split(":")
    if len(parts) == 2:
        unit, value_str = parts
        to_unit = None
    elif len(parts) == 3:
        unit, value_str, to_unit = parts
        if not to_unit:
            raise ParseError("Invalid format. Use unit:value (ex: meter:2.5)")
    else:
        raise ParseError("Invalid format. Use unit:value (ex: meter:2.5)")

    try:
        value = float(value_str)
    except ValueError as exc:
        raise ParseError(f"Invalid number: {value_str}") from exc

    return ParsedInput(unit=unit, value=value, to_unit=to_unit or None)
