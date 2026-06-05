import pytest


def test_d_t4_01_unknown_lists_supported_units(g_unknown_abc: str) -> None:
    # Given: unknown unit "abc" (G_unknown_abc, PRD F7)
    # When: registry/parser 오류 경로 호출 예정
    # Then: 오류 메시지에 meter/feet/yard 지원 목록 포함
    pytest.fail("RED: D-T4-01 — 지원 단위 목록 오류 메시지 미구현, 의도적 실패")
