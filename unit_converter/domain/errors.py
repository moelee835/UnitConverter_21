"""Domain exceptions — types only; user-facing messages stay in app (A1)."""


class UnknownUnitError(ValueError):
    """Raised when a unit id is not registered (PRD D1~D3)."""

    def __init__(self, unit: str) -> None:
        self.unit = unit
        super().__init__(unit)
