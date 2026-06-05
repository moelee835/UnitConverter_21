import pytest


def test_u_t6_01_cli_gui_same_result(g_to_yard: str) -> None:
    # Given: meter 2.5 → yard (G_to_yard, PRD G4, AC12, T6)
    # When: CLI run_session 출력 vs GUI get_result_text() 비교 예정
    # Then: 변환값·포맷 문자열 동일 (공유 control/presenter)
    pytest.fail("RED: U-T6-01 — CLI·GUI 동일 결과 미구현, 의도적 실패")
