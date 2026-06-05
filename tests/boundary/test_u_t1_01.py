from unit_converter.cli import run_session


def test_u_t1_01_cli_meters_typo_success_or_suggest(g_meters_typo: str) -> None:
    # Given: CLI 입력 "meters:2.5" (AC7 — Unknown만 금지)
    # When:
    lines: list[str] = []
    run_session(read_line=lambda _: g_meters_typo, write=lines.append)
    output = "\n".join(lines)
    # Then: 변환 3줄 또는 meter 제안; Unknown unit: meters 단독 출력 금지
    assert output != "Unknown unit: meters"
    assert len(lines) == 3 or "meter" in output.lower()
