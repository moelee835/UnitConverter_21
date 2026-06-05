"""Meter-normalized conversion to all registered units (SRP, PRD F1~F2, D4)."""

from dataclasses import dataclass

from unit_converter.domain.errors import UnknownUnitError
from unit_converter.domain.unit_registry import UnitRegistry, default_registry


@dataclass(frozen=True)
class ConversionResult:
    source_unit: str
    source_value: float
    meter_value: float
    targets: dict[str, float]


def to_meters(unit: str, value: float, registry: UnitRegistry | None = None) -> float:
    reg = registry or default_registry()
    length_unit = reg.get(unit)
    if length_unit is None:
        raise UnknownUnitError(unit)
    return length_unit.to_meter(value)


def convert_from_meters(
    meter_value: float,
    registry: UnitRegistry | None = None,
) -> dict[str, float]:
    reg = registry or default_registry()
    return {name: unit.from_meter(meter_value) for name, unit in reg.all_units().items()}


def convert(
    source_unit: str,
    value: float,
    registry: UnitRegistry | None = None,
) -> ConversionResult:
    reg = registry or default_registry()
    meter_value = to_meters(source_unit, value, reg)
    targets = convert_from_meters(meter_value, reg)
    return ConversionResult(
        source_unit=source_unit,
        source_value=value,
        meter_value=meter_value,
        targets=targets,
    )
