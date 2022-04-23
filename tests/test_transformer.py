import datetime as dt
from unittest import mock

import pandas as pd

import pytest

from meteobeguda.transformer import (
    only_one_day,
    current_temperature,
    current_humidity,
    current_pressure,
    current_wind,
    current_rain,
    utc_to_local_tz,
)


@pytest.fixture
def current_temp(eight_days):
    return current_temperature(eight_days, dt.date(2022, 3, 12))


@pytest.fixture
def current_hum(eight_days):
    return current_humidity(eight_days, dt.date(2022, 3, 12))


@pytest.fixture
def current_pres(eight_days):
    return current_pressure(eight_days, dt.date(2022, 3, 12))


@pytest.fixture
def current_wi(eight_days):
    return current_wind(eight_days)


@pytest.fixture
def current_rn(eight_days):
    return current_rain(eight_days, dt.date(2022, 3, 12))


@pytest.mark.parametrize(
    "date", [dt.date(2022, 3, 12) - dt.timedelta(k) for k in range(8)]
)
def test_only_one_day(date, eight_days):

    result = only_one_day(eight_days, date)
    assert result.timestamp.dt.date.nunique() == 1
    assert date in result.timestamp.dt.date.unique()


def test_current_temperature_min_max_are_ordered(current_temp):
    assert current_temp["min"] <= current_temp["temperature"] <= current_temp["max"]


def test_current_temperature_values(current_temp):
    expected = {
        "temperature": 10.4,
        "trend": pytest.approx(-1.1),
        "feels_like": 10.4,
        "max": 12.7,
        "max_time": dt.time(16, 30),
        "min": 8.5,
        "min_time": dt.time(9, 15),
    }
    assert expected == current_temp


def test_current_humidity_values(current_hum):
    expected = {
        "perc": 82.0,
        "max": 98.0,
        "max_time": dt.time(11, 0),
        "min": 75.0,
        "min_time": dt.time(16, 30),
    }
    assert expected == current_hum


def test_current_pressure_values(current_pres):
    expected = {
        "pressure": 1013.4,
        "trend": 1.1000000000000227,
        "max": 1014.3,
        "max_time": dt.time(0, 0),
        "min": 1011.2,
        "min_time": dt.time(5, 45),
    }
    assert expected == current_pres


def test_current_wind_values(current_wi):
    expected = {
        "direction_str": "NO",
        "direction_deg": 349,
        "speed": 0.0,
        "maxspeed": 3.2,
        "name": "Mestral"
    }
    assert expected == current_wi


def test_current_rain_values(current_rn):
    expected = {
        "today": 27.6,
        "yesterday": 3.2,
        "this_week": 37.0,
        "intensity": 0.0,
    }
    assert expected == current_rn


@pytest.mark.parametrize(
    "tz,input_value,expected_value",
    [
        (
            "Europe/London",
            pd.Timestamp("2022-02-13 09:00:00"),
            pd.Timestamp("2022-02-13 09:00:00", tz="Europe/London"),
        ),
        (
            "Europe/Madrid",
            pd.Timestamp("2022-02-13 09:00:00"),
            pd.Timestamp("2022-02-13 10:00:00", tz="Europe/Madrid"),
        ),
        (
            "Europe/London",
            pd.Timestamp("2022-04-13 09:00:00"),
            pd.Timestamp("2022-04-13 10:00:00", tz="Europe/London"),
        ),
        (
            "Europe/Madrid",
            pd.Timestamp("2022-04-13 09:00:00"),
            pd.Timestamp("2022-04-13 11:00:00", tz="Europe/Madrid"),
        ),
    ],
)
def test_convert_utc_to_local_tz(tz, input_value, expected_value):
    input_s = pd.Series([input_value])
    output_s = utc_to_local_tz(input_s, tz=tz)

    assert output_s.shape[0] == 1
    assert output_s.iloc[0] == expected_value
