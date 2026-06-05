import pytest


def test_d_t6_01_same_format_for_cli_and_gui(g_to_yard: str) -> None:
    # Given: meter 2.5 → yard (G_to_yard, PRD G4, T6)
    # When: 공유 convert+format orchestration 호출 예정
    # Then: CLI/GUI가 공유할 결정적 format 문자열 1개
    pytest.fail("RED: D-T6-01 — CLI·GUI 공유 format 미구현, 의도적 실패")
