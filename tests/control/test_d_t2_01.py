from unit_converter.app.conversion_flow import convert_parsed
from unit_converter.app.input_parser import parse_input

from tests._approval import assert_matches_golden, format_contract_output


def test_d_t2_01_yard_one_line_only(g_to_yard: str) -> None:
    # Given: parsed meter 2.5, to_unit=yard (G_to_yard, PRD F5, AC8)
    # When:
    parsed = parse_input(g_to_yard)
    lines = convert_parsed(parsed)
    # Then: yard 1줄만; feet/meter 줄 없음 (Mom Test S7·S8)
    assert len(lines) == 1
    assert "yard" in lines[0]
    assert "feet" not in lines[0]
    assert lines[0] == "2.5 meter = 2.734025 yard"

    actual = format_contract_output(
        input_raw=g_to_yard,
        status="OK",
        error="NONE",
        output_lines=lines,
        canonical_from=parsed.unit,
        canonical_to=parsed.to_unit,
    )
    assert_matches_golden(actual, "d_t2_01_g_to_yard_one_line.approved.txt")
