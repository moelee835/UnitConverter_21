"""Domain / Logic Track — PRD D*, F*, T3 (AC1~AC3)."""

import pytest

from unit_converter.domain.converter import convert, to_meters
from unit_converter.domain.unit_registry import FEET_PER_METER, YARD_PER_METER


def test_meter_to_feet_and_yard():
    result = convert("meter", 2.5)
    assert result.targets["meter"] == pytest.approx(2.5)
    assert result.targets["feet"] == pytest.approx(2.5 * FEET_PER_METER)
    assert result.targets["yard"] == pytest.approx(2.5 * YARD_PER_METER)


def test_feet_to_meter_ac2():
    assert to_meters("feet", FEET_PER_METER) == pytest.approx(1.0)


def test_yard_to_meter_ac3():
    assert to_meters("yard", YARD_PER_METER) == pytest.approx(1.0)


def test_unknown_unit_raises():
    with pytest.raises(ValueError, match="Unknown unit"):
        to_meters("abc", 1.0)
