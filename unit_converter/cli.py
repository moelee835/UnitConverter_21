"""CLI boundary (PRD A3, C1~C2) — input/print only."""

import sys
from pathlib import Path

if __name__ == "__main__" and not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unit_converter.app.conversion_flow import convert_parsed
from unit_converter.app.input_parser import ParseError, parse_input
from unit_converter.domain.unit_registry import UnitRegistry
from unit_converter.infrastructure.config_loader import create_default_registry

CLI_PROMPT = "Insert value for converting (ex: meter:2.5): "


def run_session(
    read_line=input,
    write=print,
    registry: UnitRegistry | None = None,
) -> None:
    """Interactive CLI; inject read_line/write for tests."""
    reg = registry or create_default_registry()
    raw = read_line(CLI_PROMPT)
    try:
        parsed = parse_input(raw)
    except ParseError as err:
        write(err.message)
        return

    try:
        for line in convert_parsed(parsed, reg):
            write(line)
    except ValueError as err:
        write(str(err))


def main() -> None:
    run_session()


if __name__ == "__main__":
    main()
