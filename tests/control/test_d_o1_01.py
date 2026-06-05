import json

from unit_converter.app.conversion_flow import convert_parsed
from unit_converter.app.input_parser import parse_input


def test_d_o1_01_json_single_target() -> None:
    parsed = parse_input("meter:2.5:yard:json")
    lines = convert_parsed(parsed)
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["source"] == {"unit": "meter", "value": 2.5}
    assert payload["conversions"] == [{"unit": "yard", "value": 2.734025}]


def test_d_o1_02_csv_all_units() -> None:
    parsed = parse_input("meter:2.5:csv")
    lines = convert_parsed(parsed)
    assert lines[0] == "from_unit,from_value,to_unit,to_value"
    assert any("yard" in line for line in lines[1:])
    assert any("cubit" in line for line in lines[1:])
    assert len(lines) == 5  # header + 4 units


def test_d_o1_03_table_default_unchanged(g_to_yard: str) -> None:
    parsed = parse_input(g_to_yard)
    lines = convert_parsed(parsed)
    assert len(lines) == 1
    assert lines[0] == "2.5 meter = 2.734025 yard"
