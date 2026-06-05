import pytest


def test_d_t1_01_meters_alias_to_meter(g_meters_typo: str) -> None:
    # Given: raw "meters:2.5" (G_meters_typo, Mom Test S4)
    # When: normalize_unit("meters") 호출 예정
    # Then: canonical "meter" (PRD F4, AC7, T1)
    pytest.fail("RED: D-T1-01 — normalize_unit 미구현, 의도적 실패")
