import pytest

from unit_converter.app.input_parser import ParseError, parse_input


def test_d_t4_03_negative_value_rejected(g_negative_meter: str) -> None:
    # Given: negative value (README 입력 검증, CS8)
    # When / Then: ParseError before conversion
    with pytest.raises(ParseError, match="negative"):
        parse_input(g_negative_meter)
