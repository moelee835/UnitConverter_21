from unit_converter.cli import run_session

from tests._approval import assert_matches_golden, format_contract_output


def test_u_t2_01_cli_yard_only(g_to_yard: str) -> None:
    # Given: CLI 입력 "meter:2.5:yard" (AC8, T2)
    # When:
    lines: list[str] = []
    run_session(read_line=lambda _: g_to_yard, write=lines.append)
    # Then: 출력 1줄, yard만; feet/meter 3줄 없음
    assert len(lines) == 1
    assert "yard" in lines[0]
    assert "feet" not in lines[0]
    assert lines[0] == "2.5 meter = 2.734025 yard"

    actual = format_contract_output(
        input_raw=g_to_yard,
        status="OK",
        error="NONE",
        output_lines=lines,
        canonical_to="yard",
    )
    assert_matches_golden(actual, "u_t2_01_cli_yard_only.approved.txt")
