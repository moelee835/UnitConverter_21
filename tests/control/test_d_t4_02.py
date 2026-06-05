import pytest


def test_d_t4_02_suggests_meter_for_typo(g_meterss_typo: str) -> None:
    # Given: unit 오타 "meterss" (G_meterss_typo, PRD F6, Mom Test S4)
    # When: 제안 로직 호출 예정
    # Then: "Did you mean meter?" 등 meter 제안 포함
    pytest.fail("RED: D-T4-02 — 유사 단위 제안 미구현, 의도적 실패")
