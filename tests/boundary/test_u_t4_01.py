from unit_converter.cli import run_session

from tests._approval import assert_matches_golden, format_contract_output


def _flatten_cli_lines(captured: list[str]) -> list[str]:
    flat: list[str] = []
    for chunk in captured:
        flat.extend(chunk.split("\n"))
    return flat


def test_u_t4_01_unknown_with_suggestion(g_unknown_abc: str) -> None:
    # Given: CLI 입력 "abc:1" (Mom Test S6 — 5분 재작업 전 복구)
    # When:
    lines: list[str] = []
    run_session(read_line=lambda _: g_unknown_abc, write=lines.append)
    output_lines = _flatten_cli_lines(lines)
    output = "\n".join(output_lines)
    # Then: 지원 목록 + 제안; Unknown unit 단독 출력 금지
    assert output.strip() != "Unknown unit: abc"
    assert "meter" in output
    assert "feet" in output
    assert "yard" in output
    assert "Supported units:" in output

    hint = next(
        (line for line in output_lines if line.startswith("Did you mean ")),
        None,
    )
    actual = format_contract_output(
        input_raw=g_unknown_abc,
        status="ERROR",
        error="UNKNOWN_UNIT",
        output_lines=output_lines,
        hint=hint,
    )
    assert_matches_golden(actual, "u_t4_01_unknown_with_suggestion.approved.txt")
