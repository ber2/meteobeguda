import datetime as dt
from dataclasses import dataclass
from typing import Optional, Dict

import pandas as pd


WIND_NAMES: Dict[str, str] = {
    "N": "Tramuntana",
    "NNE": "Tramuntana / Gregal",
    "NE": "Gregal",
    "ENE": "Gregal / Llevant",
    "E": "Llevant",
    "ESE": "Llevant / Xaloc",
    "SE": "Xaloc",
    "SSE": "Xaloc / Migjorn",
    "S": "Migjorn",
    "SSO": "Migjorn / Garbí",
    "SO": "Garbí",
    "OSO": "Garbí / Ponent",
    "O": "Ponent",
    "ONO": "Ponent / Mestral",
    "NO": "Mestral",
    "NNO": "Mestral / Tramuntana",
}


@dataclass
class MaxMinTime:
    max: float
    max_time: dt.time
    min: float
    min_time: dt.time


@dataclass
class CurrentTemperature:
    temperature: float
    trend: Optional[float]
    feels_like: float
    max: float
    max_time: dt.time
    min: float
    min_time: dt.time


@dataclass
class CurrentHumidity:
    perc: int
    max: int
    max_time: dt.time
    min: int
    min_time: dt.time


@dataclass
class CurrentPressure:
    pressure: float
    trend: Optional[float]
    max: float
    max_time: dt.time
    min: float
    min_time: dt.time


@dataclass
class CurrentWind:
    direction_str: str
    direction_deg: int
    speed: float
    maxspeed: float

    def name(self):
        return WIND_NAMES[self.direction_str]


@dataclass
class CurrentRain:
    today: float
    yesterday: float
    this_week: float
    intensity: float


def get_max_min_time(
    indexing_feature: str, value_feature: str, data: pd.DataFrame
) -> MaxMinTime:
    s = data.set_index(indexing_feature)[value_feature]
    return MaxMinTime(s.max(), s.idxmax().time(), s.min(), s.idxmin().time())


def last_entry(sorting_column: str, df: pd.DataFrame) -> pd.Series:
    return df.sort_values(sorting_column, ascending=False).iloc[0]


def get_trend(feature: str, data: pd.DataFrame) -> Optional[float]:
    s_last = last_entry("timestamp", data)
    last_ts = s_last.timestamp
    try:
        s_prev = data.set_index("timestamp").loc[last_ts - pd.Timedelta(hours=1)]
        trend = s_last[feature] - s_prev[feature]
    except KeyError:
        trend = None

    return trend


def only_one_day(df: pd.DataFrame, date: dt.date = dt.date.today()) -> pd.DataFrame:
    mask = df["timestamp"].dt.date == date
    return df[mask].copy()


def current_temperature(df: pd.DataFrame, date=dt.date.today()) -> CurrentTemperature:
    df_today = only_one_day(df, date)

    s_last = last_entry("timestamp", df_today)
    trend = get_trend("temperature", df_today)
    mmd = get_max_min_time("timestamp", "temperature", df_today)

    return CurrentTemperature(
        s_last.temperature,
        trend,
        s_last.temperature_feeling,
        mmd.max,
        mmd.max_time,
        mmd.min,
        mmd.min_time,
    )


def current_humidity(df: pd.DataFrame, date=dt.date.today()) -> CurrentHumidity:
    df_today = only_one_day(df, date)
    s_last = last_entry("timestamp", df_today)
    mmd = get_max_min_time("timestamp", "humidity", df_today)
    return CurrentHumidity(
        s_last.humidity, int(mmd.max), mmd.max_time, int(mmd.min), mmd.min_time
    )


def current_pressure(df: pd.DataFrame, date=dt.date.today()) -> CurrentPressure:
    df_today = only_one_day(df, date)

    s_last = last_entry("timestamp", df_today)
    trend = get_trend("pressure", df_today)
    mmd = get_max_min_time("timestamp", "pressure", df_today)

    return CurrentPressure(
        s_last.pressure, trend, mmd.max, mmd.max_time, mmd.min, mmd.min_time
    )


def current_wind(df: pd.DataFrame) -> CurrentWind:
    s_last = last_entry("timestamp", df)
    return CurrentWind(
        s_last.wind_direction,
        s_last.tx_wind,
        s_last.windspeed,
        s_last.windspeed_max,
    )


def current_rain(df: pd.DataFrame, date: dt.date = dt.date.today()) -> CurrentRain:

    rain_today = df[df.timestamp.dt.date == date].rain.sum()
    rain_yesterday = df[df.timestamp.dt.date == (date - dt.timedelta(1))].rain.sum()
    total_rain = df.rain.sum()
    s_last = last_entry("timestamp", df)
    intensity = s_last.rain_intensity
    return CurrentRain(rain_today, rain_yesterday, total_rain, intensity)
