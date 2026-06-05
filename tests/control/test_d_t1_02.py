import pytest


def test_d_t1_02_parse_input_trims_whitespace(g_meter_trimmed: str) -> None:
    # Given: raw " meter : 2.5 " (공백 trim, PRD AC9)
    # When: parse_input(g_meter_trimmed) 호출 예정
    # Then: unit="meter", value=2.5, 오류 없음 (F4, I6)
    pytest.fail("RED: D-T1-02 — parse_input trim 미구현, 의도적 실패")
