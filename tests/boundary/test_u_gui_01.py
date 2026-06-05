import pytest


def test_u_gui_01_entry_point_importable() -> None:
    # Given: GUI boundary 미구현 (PRD G5, A5 — PyQt6 진입점 분리)
    # When: gui_boundary import 및 main()/UnitConverterWindow 존재 확인 예정
    # Then: python -m unit_converter.gui 진입 가능; app/domain에 PyQt6 없음 (AC11)
    pytest.fail("RED: U-GUI-01 — gui_boundary 진입점 미구현, 의도적 실패")
