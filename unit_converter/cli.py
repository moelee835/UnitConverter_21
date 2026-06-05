"""CLI boundary (PRD A3, C1~C2) — input/print only."""

import sys
from pathlib import Path

if __name__ == "__main__" and not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unit_converter.app.conversion_flow import convert_parsed
from unit_converter.app.input_parser import ParseError, parse_input


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
        for line in convert_parsed(parsed):
            write(line)
    except ValueError as err:
        write(str(err))


def main() -> None:
    run_session()


if __name__ == "__main__":
    main()
