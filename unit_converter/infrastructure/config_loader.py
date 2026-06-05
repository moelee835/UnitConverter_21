"""JSON configuration loader — PRD §2.3, §11 v0.4 (Improvement_Roadmap Sprint C1)."""

from __future__ import annotations

import json
from pathlib import Path

from unit_converter.domain.unit_registry import UnitRegistry

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONFIG_PATH = _PROJECT_ROOT / "config" / "units.json"


def load_config(path: str | None = None) -> dict:
    config_path = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    return json.loads(config_path.read_text(encoding="utf-8"))


def create_default_registry() -> UnitRegistry:
    return UnitRegistry.from_config(load_config())
