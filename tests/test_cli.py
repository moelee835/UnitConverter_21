"""Boundary / UI Track — PRD C*, AC1."""

from unit_converter.cli import run_session


def test_meter_2_5_prints_three_lines(capsys):
    lines: list[str] = []

    def fake_input(_prompt: str) -> str:
        return "meter:2.5"

    def fake_write(msg: str) -> None:
        lines.append(msg)

    run_session(read_line=fake_input, write=fake_write)

    assert len(lines) == 3
    assert all("2.5 meter =" in line for line in lines)
    assert any("feet" in line for line in lines)
    assert any("yard" in line for line in lines)
