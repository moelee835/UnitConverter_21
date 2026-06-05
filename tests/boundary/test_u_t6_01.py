from unit_converter.cli import run_session
from unit_converter.gui_boundary import UnitConverterWindow


def test_u_t6_01_cli_gui_same_result(g_to_yard: str) -> None:
    # Given: meter 2.5 → yard (G_to_yard, PRD G4, AC12, T6)
    # When: CLI run_session 출력 vs GUI get_result_text() 비교
    cli_lines: list[str] = []
    run_session(read_line=lambda _: g_to_yard, write=cli_lines.append)
    window = UnitConverterWindow()
    window.apply_input(g_to_yard)
    gui_text = window.get_result_text()
    # Then: 변환값·포맷 문자열 동일 (공유 control/presenter)
    assert len(cli_lines) == 1
    assert gui_text == cli_lines[0]
    assert gui_text == "2.5 meter = 2.734025 yard"
