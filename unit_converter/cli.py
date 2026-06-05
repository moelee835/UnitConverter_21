"""CLI boundary (PRD A3, C1~C2) — input/print only."""

import sys
from pathlib import Path

if __name__ == "__main__" and not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unit_converter.app.input_parser import ParseError, parse_input
from unit_converter.app.output_formatter import format_all_lines, format_single_line
from unit_converter.domain.converter import convert
from unit_converter.domain.converter import to_meters as domain_to_meters


def run_session(
    read_line=input,
    write=print,
) -> None:
    """Interactive CLI; inject read_line/write for tests."""
    raw = read_line("Insert value for converting (ex: meter:2.5): ")
    try:
        parsed = parse_input(raw)
    except ParseError as err:
        write(err.message)
        return

    try:
        if parsed.to_unit:
            result = convert(parsed.unit, parsed.value)
            line = format_single_line(result, parsed.to_unit)
            if line is None:
                write(f"Unknown unit: {parsed.to_unit}")
                return
            write(line)
        else:
            domain_to_meters(parsed.unit, parsed.value)
            result = convert(parsed.unit, parsed.value)
            for line in format_all_lines(result):
                write(line)
    except ValueError as err:
        write(str(err))


def main() -> None:
    run_session()


if __name__ == "__main__":
    main()
