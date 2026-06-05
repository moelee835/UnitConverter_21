from unit_converter.app.conversion_flow import convert_parsed
from unit_converter.app.input_parser import parse_input


def test_d_t6_01_same_format_for_cli_and_gui(g_to_yard: str) -> None:
    # Given: meter 2.5 → yard (G_to_yard, PRD G4, T6)
    # When:
    parsed = parse_input(g_to_yard)
    lines = convert_parsed(parsed)
    # Then: CLI/GUI가 공유할 결정적 format 문자열 1개
    assert len(lines) == 1
    assert lines[0] == "2.5 meter = 2.734025 yard"
