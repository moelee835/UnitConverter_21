"""Shared fixtures for RED/GREEN tests — data only, no Domain Mock."""

import pytest


@pytest.fixture
def g_meter_2_5() -> str:
    return "meter:2.5"


@pytest.fixture
def g_meters_typo() -> str:
    return "meters:2.5"


@pytest.fixture
def g_meter_trimmed() -> str:
    return " meter : 2.5 "


@pytest.fixture
def g_to_yard() -> str:
    return "meter:2.5:yard"


@pytest.fixture
def g_unknown_abc() -> str:
    return "abc:1"


@pytest.fixture
def g_meterss_typo() -> str:
    return "meterss:1"


@pytest.fixture
def g_negative_meter() -> str:
    return "meter:-2.5"


@pytest.fixture
def g_app_module_names() -> list[str]:
    return ["input_parser", "output_formatter", "conversion_flow"]


@pytest.fixture
def g_domain_module_names() -> list[str]:
    return ["converter", "unit_registry"]


@pytest.fixture(scope="session")
def qapp():
    """Headless QApplication for GUI boundary tests (Phase 5)."""
    from PyQt6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
