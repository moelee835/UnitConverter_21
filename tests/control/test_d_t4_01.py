from unit_converter.app.input_parser import format_unknown_unit_message, parse_input

from tests._approval import assert_matches_golden, format_contract_output


def test_d_t4_01_unknown_lists_supported_units(g_unknown_abc: str) -> None:
    # Given: unknown unit "abc" (G_unknown_abc, PRD F7)
    # When:
    parsed = parse_input(g_unknown_abc)
    message = format_unknown_unit_message(parsed.unit)
    error_lines = message.split("\n")
    # Then: 오류 메시지에 meter/feet/yard 지원 목록 포함
    assert "meter" in message
    assert "feet" in message
    assert "yard" in message
    assert "cubit" in message
    assert "Supported units:" in message

    hint = next(
        (line.removeprefix("Did you mean ").removesuffix("?") for line in error_lines if line.startswith("Did you mean ")),
        None,
    )
    actual = format_contract_output(
        input_raw=g_unknown_abc,
        status="ERROR",
        error="UNKNOWN_UNIT",
        output_lines=error_lines,
        hint=f"Did you mean {hint}?" if hint else None,
    )
    assert_matches_golden(actual, "d_t4_01_unknown_abc.approved.txt")
