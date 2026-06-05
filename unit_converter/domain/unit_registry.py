"""Unit registration and lookup — v0.3 OCP core; v0.2 built-in meter/feet/yard."""

from dataclasses import dataclass

from unit_converter.domain.length_unit import LengthUnit, UnitId

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


def create_builtin_unit(unit_id: str, to_meter_factor: float) -> LengthUnit:
    """Factory for built-in style units (v0.4 runtime registration)."""
    return _BuiltinUnit(unit_id, to_meter_factor, to_meter_factor)


class UnitRegistry:
    """Lookup by canonical unit id (PRD D1~D3)."""

    def __init__(
        self,
        units: dict[str, LengthUnit] | None = None,
        *,
        aliases: dict[str, str] | None = None,
        suggest_cutoff: float = 0.6,
    ) -> None:
        self._units = dict(units if units is not None else _BUILTIN)
        self._aliases = dict(aliases if aliases is not None else {})
        self._suggest_cutoff = suggest_cutoff

    @classmethod
    def from_config(cls, config: dict) -> UnitRegistry:
        units: dict[str, LengthUnit] = {}
        for entry in config["units"]:
            units[entry["id"]] = _BuiltinUnit(
                entry["id"],
                entry["to_meter_factor"],
                entry["from_meter_factor"],
            )
        return cls(
            units,
            aliases=config.get("aliases", {}),
            suggest_cutoff=config.get("suggest_cutoff", 0.6),
        )

    def get(self, name: str) -> LengthUnit | None:
        return self._units.get(name)

    def names(self) -> list[str]:
        return sorted(self._units.keys())

    def all_units(self) -> dict[str, LengthUnit]:
        return dict(self._units)

    def resolve_alias(self, raw: str) -> UnitId:
        """Canonical unit id from alias (PRD F4, CS10)."""
        key = raw.strip().lower()
        return self._aliases.get(key, key)

    def alias_keys(self) -> list[str]:
        return list(self._aliases.keys())

    def suggest_cutoff(self) -> float:
        return self._suggest_cutoff

    def register(self, unit: LengthUnit) -> None:
        """Runtime unit registration (PRD v0.4 — config 외 추가)."""
        self._units[unit.name] = unit


def default_registry() -> UnitRegistry:
    from unit_converter.infrastructure.config_loader import create_default_registry

    return create_default_registry()
