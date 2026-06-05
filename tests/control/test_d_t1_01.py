from unit_converter.app.input_parser import normalize_unit

from tests._approval import assert_matches_golden, format_contract_output


def test_d_t1_01_meters_alias_to_meter(g_meters_typo: str) -> None:
    # Given: raw "meters:2.5" (G_meters_typo, Mom Test S4)
    # When:
    result = normalize_unit("meters")
    # Then: canonical "meter" (PRD F4, AC7, T1)
    assert result == "meter"

    actual = format_contract_output(
        input_raw="meters",
        status="OK",
        error="NONE",
        output_lines=[],
        canonical_from=result,
    )
    assert_matches_golden(actual, "d_t1_01_meters_alias.approved.txt")
