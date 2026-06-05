"""Input parsing (PRD parser) — I1, I3, I4; F4/I6 in Phase 1."""

import difflib
from dataclasses import dataclass

from unit_converter.domain.unit_registry import default_registry


class ParseError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class ParsedInput:
    unit: str
    value: float
    to_unit: str | None = None


_UNIT_ALIASES = {"meters": "meter"}


def normalize_unit(raw: str) -> str:
    """Canonical unit id from alias (PRD F4, AC7). Phase 1: meters→meter."""
    u = raw.strip().lower()
    return _UNIT_ALIASES.get(u, u)


def suggest_unit(raw: str) -> str | None:
    """Closest canonical unit for typos (PRD F6)."""
    reg = default_registry()
    candidates = list(reg.names()) + list(_UNIT_ALIASES.keys())
    normalized = raw.strip().lower()
    matches = difflib.get_close_matches(normalized, candidates, n=1, cutoff=0.6)
    if not matches:
        return None
    return normalize_unit(matches[0])


def format_unknown_unit_message(unit: str) -> str:
    """Unknown unit error with supported list and optional suggestion (PRD F6, F7)."""
    reg = default_registry()
    supported = ", ".join(reg.names())
    lines = [f"Unknown unit: {unit}", f"Supported units: {supported}"]
    suggestion = suggest_unit(unit)
    if suggestion:
        lines.append(f"Did you mean {suggestion}?")
    return "\n".join(lines)


def parse_input(raw: str) -> ParsedInput:
    """Parse `{from_unit}:{value}` (PRD I1). `from:value:to` — Phase 2."""
    if ":" not in raw:
        raise ParseError("Invalid format. Use unit:value (ex: meter:2.5)")

    parts = [part.strip() for part in raw.split(":")]
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

    unit = normalize_unit(unit)
    if to_unit is not None:
        to_unit = normalize_unit(to_unit)

    return ParsedInput(unit=unit, value=value, to_unit=to_unit)
