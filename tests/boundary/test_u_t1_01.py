import pytest


def test_u_t1_01_cli_meters_typo_success_or_suggest(g_meters_typo: str) -> None:
    # Given: CLI 입력 "meters:2.5" (AC7 — Unknown만 금지)
    # When: run_session(read_line=…, write=…) 호출 예정
    # Then: 변환 3줄 또는 meter 제안; Unknown unit: meters 단독 출력 금지
    pytest.fail("RED: U-T1-01 — meters 별칭/제안 미구현, 의도적 실패")
