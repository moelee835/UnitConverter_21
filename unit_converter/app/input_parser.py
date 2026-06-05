"""Input parsing (PRD parser) — I1, I3, I4; F4/I6 in Phase 1."""

import difflib
from dataclasses import dataclass
from typing import Literal

from unit_converter.domain.unit_registry import default_registry

OutputFormat = Literal["table", "json", "csv"]
VALID_OUTPUT_FORMATS = frozenset({"table", "json", "csv"})


class ParseError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class ParsedInput:
    unit: str
    value: float
    to_unit: str | None = None
    output_format: OutputFormat = "table"


def _parse_output_format(raw: str) -> OutputFormat:
    fmt = raw.strip().lower()
    if fmt not in VALID_OUTPUT_FORMATS:
        raise ParseError(f"Invalid output format: {raw}. Use table, json, or csv")
    return fmt  # type: ignore[return-value]


def _is_output_format(part: str) -> bool:
    return part.strip().lower() in VALID_OUTPUT_FORMATS


def normalize_unit(raw: str) -> str:
    """Canonical unit id from alias (PRD F4, AC7)."""
    return default_registry().resolve_alias(raw)


def suggest_unit(raw: str) -> str | None:
    """Closest canonical unit for typos (PRD F6)."""
    reg = default_registry()
    candidates = list(reg.names()) + reg.alias_keys()
    normalized = raw.strip().lower()
    matches = difflib.get_close_matches(
        normalized, candidates, n=1, cutoff=reg.suggest_cutoff()
    )
    if not matches:
        return None
    return normalize_unit(matches[0])


def parse_input(raw: str) -> ParsedInput:
    """Parse `{from_unit}:{value}` (PRD I1). `from:value:to` — Phase 2."""
    if ":" not in raw:
        raise ParseError("Invalid format. Use unit:value (ex: meter:2.5)")

    parts = [part.strip() for part in raw.split(":")]
    output_format: OutputFormat = "table"
    if len(parts) == 2:
        unit, value_str = parts
        to_unit = None
    elif len(parts) == 3:
        unit, value_str, third = parts
        if _is_output_format(third):
            to_unit = None
            output_format = _parse_output_format(third)
        else:
            to_unit = third
    elif len(parts) == 4:
        unit, value_str, to_unit, fmt = parts
        output_format = _parse_output_format(fmt)
        if not to_unit:
            raise ParseError("Invalid format. Use unit:value:to_unit:format")
    else:
        raise ParseError("Invalid format. Use unit:value (ex: meter:2.5)")

    try:
        value = float(value_str)
    except ValueError as exc:
        raise ParseError(f"Invalid number: {value_str}") from exc

    if value < 0:
        raise ParseError(f"Invalid number: negative values are not supported")

    unit = normalize_unit(unit)
    if to_unit is not None:
        to_unit = normalize_unit(to_unit)

    return ParsedInput(
        unit=unit,
        value=value,
        to_unit=to_unit,
        output_format=output_format,
    )


# Backward-compatible re-export (tests import from input_parser)
from unit_converter.app.output_formatter import format_unknown_unit_message  # noqa: E402,F401
