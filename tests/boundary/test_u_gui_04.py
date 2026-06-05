import pytest


def test_u_gui_04_inline_error_feedback(qapp, g_unknown_abc: str) -> None:
    # Given: 잘못된 단위 "abc" (G_unknown_abc, PRD G3, F7 — P1)
    # When: GUI Convert 클릭 후 인라인 오류 영역 검사 예정
    # Then: 위젯 내 오류·지원 단위 표시; 별도 Unknown-only 금지
    pytest.fail("RED: U-GUI-04 — GUI 인라인 오류 피드백 미구현, 의도적 실패")
