"""Length unit contract (Protocol) — v0.3 OCP extension; v0.2 built-in units only."""

from typing import Protocol


class LengthUnit(Protocol):
    """PRD D1~D4: unit name and conversion to meters."""

    @property
    def name(self) -> str:
        ...

    def to_meter(self, value: float) -> float:
        ...

    def from_meter(self, meter_value: float) -> float:
        ...
