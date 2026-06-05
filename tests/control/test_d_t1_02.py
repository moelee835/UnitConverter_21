from unit_converter.app.input_parser import parse_input


def test_d_t1_02_parse_input_trims_whitespace(g_meter_trimmed: str) -> None:
    # Given: raw " meter : 2.5 " (공백 trim, PRD AC9)
    # When:
    result = parse_input(g_meter_trimmed)
    # Then: unit="meter", value=2.5, 오류 없음 (F4, I6)
    assert result.unit == "meter"
    assert result.value == 2.5
    assert result.to_unit is None
