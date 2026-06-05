"""Unit registration and lookup — v0.3 OCP core; v0.2 built-in meter/feet/yard."""

from dataclasses import dataclass

from unit_converter.domain.length_unit import LengthUnit

FEET_PER_METER = 3.28084
YARD_PER_METER = 1.09361


@dataclass(frozen=True)
class _BuiltinUnit:
    name: str
    to_meter_factor: float
    from_meter_factor: float

    def to_meter(self, value: float) -> float:
        return value / self.to_meter_factor

    def from_meter(self, meter_value: float) -> float:
        return meter_value * self.from_meter_factor


_BUILTIN: dict[str, LengthUnit] = {
    "meter": _BuiltinUnit("meter", 1.0, 1.0),
    "feet": _BuiltinUnit("feet", FEET_PER_METER, FEET_PER_METER),
    "yard": _BuiltinUnit("yard", YARD_PER_METER, YARD_PER_METER),
}


class UnitRegistry:
    """Lookup by canonical unit id (PRD D1~D3)."""

    def __init__(self, units: dict[str, LengthUnit] | None = None) -> None:
        self._units = dict(units if units is not None else _BUILTIN)

    def get(self, name: str) -> LengthUnit | None:
        return self._units.get(name)

    def names(self) -> list[str]:
        return sorted(self._units.keys())

    def all_units(self) -> dict[str, LengthUnit]:
        return dict(self._units)


def default_registry() -> UnitRegistry:
    return UnitRegistry()
