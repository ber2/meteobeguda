import os
import datetime as dt
from typing import Callable

import typer

from meteobeguda.fetcher import get_last_two_days, get_last_eight_days
from meteobeguda.parser import parse_response, parse_timestamps
from meteobeguda.transformer import only_one_day

app = typer.Typer()


def select_fetcher(lookback: int) -> Callable:
    if lookback <= 1:
        return get_last_two_days
    return get_last_eight_days


@app.command()
def extract(lookback: int = 1) -> None:
    print(f"Lookback {lookback}")
    if lookback < 1:
        raise ValueError("Lookback should be at least 1")
    if lookback > 7:
        raise ValueError("Lookback should be at most 7")

    fetcher = select_fetcher(lookback)

    raw = fetcher()
    df = parse_response(raw)
    parse_timestamps(df)

    dates = [dt.date.today() - dt.timedelta(k) for k in range(1, lookback + 1)]
    for date in dates:
        df_one_day = only_one_day(df, date)
        path = "data/" + date.strftime("%Y/%m")
        os.system(f"mkdir -p {path}")
        df_one_day.to_parquet(f"{path}/meteolocal-{date.isoformat()}.parquet")


if __name__ == "__main__":
    app()
