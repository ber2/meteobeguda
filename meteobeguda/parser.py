from io import BytesIO

import pandas as pd
import numpy as np

from .fetcher import get_last_two_days


COLUMNS = {
    "date": np.dtype("O"),
    "time": np.dtype("O"),
    "temperature": np.dtype("float64"),
    "temperature_max": np.dtype("float64"),
    "temperature_min": np.dtype("float64"),
    "humidity": np.dtype("int64"),
    "dew": np.dtype("float64"),
    "windspeed": np.dtype("float64"),
    "wind_direction": pd.StringDtype(),
    "wind_rec": np.dtype("float64"),
    "windspeed_max": np.dtype("float64"),
    "windspeed_max_direction": pd.StringDtype(),
    "temperature_feeling": np.dtype("float64"),
    "heat_index": np.dtype("float64"),
    "thw_index": np.dtype("float64"),
    "pressure": np.dtype("float64"),
    "rain": np.dtype("float64"),
    "rain_intensity": np.dtype("float64"),
    "heat_degrees": np.dtype("float64"),
    "cold_degrees": np.dtype("float64"),
    "temperature_interior": np.dtype("float64"),
    "humidity_interior": np.dtype("int64"),
    "dew_interior": np.dtype("float64"),
    "heat_index_interior": np.dtype("float64"),
    "air_density_interior": np.dtype("float64"),
    "wind_direction_degrees": np.dtype("float64"),
    "tx_wind": np.dtype("int64"),
    "iss_reception": np.dtype("int64"),
    "arc_interior": np.dtype("float64"),
}


def parse_response(raw: bytes) -> pd.DataFrame:
    return pd.read_csv(
        BytesIO(raw),
        sep=r"\s+",
        header=None,
        skiprows=3,
        encoding="latin1",
        names=COLUMNS.keys(),
        index_col=False,
        dtype=COLUMNS,
    )


def parse_timestamps(data: pd.DataFrame) -> None:
    data["timestamp"] = pd.to_datetime(data["date"] + " " + data["time"], dayfirst=True)
    data.drop(["date", "time"], axis=1, inplace=True)
