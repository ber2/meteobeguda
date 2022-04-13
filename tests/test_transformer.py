import datetime as dt
from unittest import mock

import pytest

from meteobeguda.transformer import (
    only_one_day,
    current_temperature,
    current_humidity,
    current_pressure,
    current_wind,
    current_rain,
)


@pytest.mark.parametrize(
    "date", [dt.date(2022, 3, 12) - dt.timedelta(k) for k in range(8)]
)
def test_only_one_day(date, eight_days):

    result = only_one_day(eight_days, date)
    assert result.timestamp.dt.date.nunique() == 1
    assert date in result.timestamp.dt.date.unique()


@pytest.fixture
def current_temp(eight_days):
    return current_temperature(eight_days, dt.date(2022, 3, 12))


def test_current_temperature_min_max_are_ordered(current_temp):
    assert current_temp.min <= current_temp.temperature <= current_temp.max


def check_dataclass_attr(instance, attr_name, expected_value):
    actual_value = getattr(instance, attr_name)
    assert expected_value == actual_value


@pytest.mark.parametrize(
    "name,expected_value",
    [
        ("temperature", 10.4),
        ("trend", pytest.approx(-1.1)),
        ("feels_like", 10.4),
        ("max", 12.7),
        ("max_time", dt.time(16, 30)),
        ("min", 8.5),
        ("min_time", dt.time(9, 15)),
    ],
)
def test_current_temperature_values(name, expected_value, current_temp):
    check_dataclass_attr(current_temp, name, expected_value)


@pytest.fixture
def current_hum(eight_days):
    return current_humidity(eight_days, dt.date(2022, 3, 12))


@pytest.mark.parametrize(
    "name,expected_value",
    [
        ("perc", 82.0),
        ("max", 98.0),
        ("max_time", dt.time(11, 0)),
        ("min", 75.0),
        ("min_time", dt.time(16, 30)),
    ],
)
def test_current_humidity_values(name, expected_value, current_hum):
    check_dataclass_attr(current_hum, name, expected_value)


@pytest.fixture
def current_pres(eight_days):
    return current_pressure(eight_days, dt.date(2022, 3, 12))


@pytest.mark.parametrize(
    "name,expected_value",
    [
        ("pressure", 1013.4),
        ("trend", 1.1000000000000227),
        ("max", 1014.3),
        ("max_time", dt.time(0, 0)),
        ("min", 1011.2),
        ("min_time", dt.time(5, 45)),
    ],
)
def test_current_pressure_values(name, expected_value, current_pres):
    check_dataclass_attr(current_pres, name, expected_value)


@pytest.fixture
def current_wi(eight_days):
    return current_wind(eight_days)


@pytest.mark.parametrize(
    "name,expected_value",
    [
        ("direction_str", "NO"),
        ("direction_deg", 349),
        ("speed", 0.0),
        ("maxspeed", 3.2),
    ],
)
def test_current_wind_values(name, expected_value, current_wi):
    check_dataclass_attr(current_wi, name, expected_value)


@pytest.fixture
def current_rn(eight_days):
    return current_rain(eight_days, dt.date(2022, 3, 12))


@pytest.mark.parametrize(
    "name,expected_value",
    [
        ("today", 27.6),
        ("yesterday", 3.2),
        ("this_week", 37.0),
        ("intensity", 0.0),
    ],
)
def test_current_rain_values(name, expected_value, current_rn):
    check_dataclass_attr(current_rn, name, expected_value)
