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

    def _daily_plot(
        self,
        value_col: str,
        title: str,
        y_label: str,
        range_y: Optional[List[int]] = None,
    ):
        d = self.df.copy()
        d["date"] = d.timestamp.dt.date
        d_agg = (
            d.groupby("date")[value_col]
            .agg(["max", "mean", "min"])
            .reset_index()
            .rename(columns={"max": "Màxima", "mean": "Mitjana", "min": "Mínima"})
        )
        fig = px.line(
            d_agg,
            x="date",
            y=["Màxima", "Mitjana", "Mínima"],
            title=title,
            labels={"date": "Data", "value": y_label},
            range_y=range_y,
            color_discrete_sequence=["#EF553B", "#00CC96", "#636EFA"],
        )
        fig.update_layout(showlegend=False)
        return st.plotly_chart(fig)

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

    def temperature_daily_line_plot(self):
        return self._daily_plot(
            value_col="temperature",
            title="Temperatures diàries",
            y_label="Temperatura",
            range_y=[-5.0, 45.0],
        )

    def humidity_daily_line_plot(self):
        return self._daily_plot(
            value_col="humidity",
            title="Humitat diària",
            y_label="Humitat (%)",
            range_y=[0.0, 100.0],
        )

    def windspeed_daily_line_plot(self):
        return self._daily_plot(
            value_col="windspeed_max",
            title="Velocitat màxima del vent diària",
            y_label="Velocitat (km/h)",
        )

    def pressure_daily_line_plot(self):
        return self._daily_plot(
            value_col="pressure",
            title="Pressió atmosfèrica diària",
            y_label="Pressió (hPa)",
            range_y=[980.0, 1030.0],
        )
