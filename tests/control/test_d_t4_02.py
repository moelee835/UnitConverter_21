from unit_converter.app.input_parser import format_unknown_unit_message, parse_input, suggest_unit


def test_d_t4_02_suggests_meter_for_typo(g_meterss_typo: str) -> None:
    # Given: unit 오타 "meterss" (G_meterss_typo, PRD F6, Mom Test S4)
    # When:
    parsed = parse_input(g_meterss_typo)
    suggestion = suggest_unit(parsed.unit)
    message = format_unknown_unit_message(parsed.unit)
    # Then: "Did you mean meter?" 등 meter 제안 포함
    assert suggestion == "meter"
    assert "Did you mean meter?" in message
