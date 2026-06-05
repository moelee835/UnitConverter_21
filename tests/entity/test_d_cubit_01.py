"""Domain / config — cubit loaded from units.json (Sprint D v0.4)."""

import pytest

from unit_converter.domain.converter import convert, to_meters
from unit_converter.infrastructure.config_loader import create_default_registry


def test_cubit_from_config_registry() -> None:
    reg = create_default_registry()
    assert "cubit" in reg.names()


def test_cubit_to_meter_via_config() -> None:
    reg = create_default_registry()
    # 1 cubit ≈ 0.524 m (Royal Egyptian cubit, config SSOT)
    assert to_meters("cubit", reg.get("cubit").to_meter_factor, reg) == pytest.approx(1.0)


def test_meter_to_cubit_in_targets() -> None:
    reg = create_default_registry()
    result = convert("meter", 0.524, reg)
    assert "cubit" in result.targets
    assert result.targets["cubit"] == pytest.approx(1.0)


def test_runtime_register_unit() -> None:
    from unit_converter.domain.unit_registry import UnitRegistry, create_builtin_unit

    reg = UnitRegistry(units={"meter": create_builtin_unit("meter", 1.0)})
    reg.register(create_builtin_unit("span", 2.0))
    assert "span" in reg.names()
    assert to_meters("span", 2.0, reg) == pytest.approx(1.0)
