"""Boundary / UI Track — PRD C*, AC1."""

from unit_converter.cli import run_session

from tests._approval import assert_matches_golden, format_contract_output


def test_meter_2_5_prints_three_lines(capsys):
    input_raw = "meter:2.5"
    lines: list[str] = []

    def fake_input(_prompt: str) -> str:
        return input_raw

    def fake_write(msg: str) -> None:
        lines.append(msg)

    run_session(read_line=fake_input, write=fake_write)

    assert len(lines) == 3
    assert all("2.5 meter =" in line for line in lines)
    assert any("feet" in line for line in lines)
    assert any("yard" in line for line in lines)

    actual = format_contract_output(
        input_raw=input_raw,
        status="OK",
        error="NONE",
        output_lines=lines,
    )
    assert_matches_golden(actual, "d_t3_01_meter_2_5_three_lines.approved.txt")
