"""Shared fixtures for RED/GREEN tests — data only, no Domain Mock."""

import pytest


@pytest.fixture
def g_meter_2_5() -> str:
    return "meter:2.5"


@pytest.fixture
def g_meters_typo() -> str:
    return "meters:2.5"


@pytest.fixture
def g_to_yard() -> str:
    return "meter:2.5:yard"


@pytest.fixture
def g_app_module_names() -> list[str]:
    return ["input_parser", "output_formatter"]


@pytest.fixture
def g_domain_module_names() -> list[str]:
    return ["converter", "unit_registry"]
