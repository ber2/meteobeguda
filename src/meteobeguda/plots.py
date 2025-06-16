import datetime as dt
from typing import Optional, List

import pandas as pd
import plotly.express as px
import streamlit as st


class Plotter:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def _ts_line_plot(self, y: str, y_label: str, range_y: Optional[List[int]] = None):
        labels = {"timestamp": "Data", y: y_label}
        return st.plotly_chart(
            px.line(self.df, x="timestamp", y=y, labels=labels, range_y=range_y)
        )

    def temperature_line_plot(self):
        return self._ts_line_plot(
            "temperature", "Temperatura (C)", range_y=[-5.0, 45.0]
        )

    def temperature_daily_line_plot(self):
        d = self.df.copy()
        d["date"] = d.timestamp.dt.date
        d_agg = (
            d.groupby("date")
            .temperature.agg(["max", "mean", "min"])
            .reset_index()
            .rename(columns={"max": "Màxima", "mean": "Mitjana", "min": "Mínima"})
        )
        return st.plotly_chart(
            px.line(
                d_agg,
                x="date",
                y=["Màxima", "Mitjana", "Mínima"],
                title="Temperatures diàries",
                labels={"date": "Data", "value": "Temperatura"},
                range_y=[-5.0, 45.0],
                color_discrete_sequence=["red", "green", "blue"],
            )
        )

    def humidity_line_plot(self):
        return self._ts_line_plot("humidity", "Humitat (%)", range_y=[0.0, 100.0])

    def pressure_line_plot(self):
        return self._ts_line_plot(
            "pressure", "Pressió atmosfèrica (hPa)", range_y=[980.0, 1030.0]
        )

    def rain_hourly_bar_plot(self, date: dt.date = dt.date.today()):
        d = self.df.copy()
        d_agg = d.resample("H", on="timestamp").rain.agg("sum").reset_index()

        return st.plotly_chart(
            px.bar(
                d_agg,
                x="timestamp",
                y="rain",
                title="Pluja per hora",
                labels={"hour": "Hora", "rain": "Pluja (mm)"},
            )
        )

    def rain_daily_bar_plot(self):
        d = self.df.copy()
        d["date"] = d.timestamp.dt.date
        d_agg = d.groupby("date").rain.agg("sum").reset_index()

        return st.plotly_chart(
            px.bar(
                d_agg,
                x="date",
                y="rain",
                title="Pluja per dia",
                labels={"date": "Data", "rain": "Pluja (mm)"},
            )
        )

    def windspeed_line_plot(self):
        return self._ts_line_plot("windspeed_max", "Velocitat màxima del vent")
