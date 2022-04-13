import datetime as dt

import streamlit as st
import pandas as pd

from meteobeguda.fetcher import get_last_eight_days
from meteobeguda.parser import parse_response, parse_timestamps
from meteobeguda.transformer import (
    current_temperature,
    current_humidity,
    current_pressure,
    current_wind,
    current_rain,
    utc_to_local_tz,
)
from meteobeguda.plots import Plotter


@st.experimental_memo
def load_live() -> pd.DataFrame:
    raw = get_last_eight_days()
    df = parse_response(raw)
    parse_timestamps(df)
    df["timestamp"] = utc_to_local_tz(df["timestamp"])
    return df


data = load_live()
plotter = Plotter(data)

hour_str = lambda x: x.strftime("%H:%M")
st.header("Temperatura")
current_temp = current_temperature(data)

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "", f"{current_temp.temperature:.1f} C", delta=f"{current_temp.trend:.1f} C"
)
col2.metric(f"Mínima {hour_str(current_temp.min_time)}", f"{current_temp.min:.1f} C")
col3.metric(f"Màxima {hour_str(current_temp.max_time)}", f"{current_temp.max:.1f} C")
col4.metric("Sensació", f"{current_temp.feels_like:.1f} C")

plotter.temperature_line_plot()

st.header("Pluja")

rain = current_rain(data)

col1, col2, col3 = st.columns(3)
col1.metric("Avui", f"{rain.today:.1f} mm")
col2.metric("Ahir", f"{rain.yesterday:.1f} mm")
col3.metric("Aquesta setmana", f"{rain.this_week:.1f} mm")
col1.metric("Intensitat", f"{rain.intensity} mm / hora")

plotter.rain_hourly_bar_plot()
plotter.rain_daily_bar_plot()

st.header("Humitat")
current_hum = current_humidity(data)

col1, col2, col3 = st.columns(3)
col1.metric("", f"{current_hum.perc} %")
col2.metric(f"Mínima {hour_str(current_hum.min_time)}", f"{current_hum.min:.1f} %")
col3.metric(f"Màxima {hour_str(current_hum.max_time)}", f"{current_hum.max:.1f} %")

plotter.humidity_line_plot()

st.header("Pressió atmosfèrica")
current_press = current_pressure(data)

col1, col2, col3 = st.columns(3)
col1.metric("", f"{current_press.pressure} hPa", delta=f"{current_press.trend:.1f} hPa")
col2.metric(
    f"Mínima {hour_str(current_press.min_time)}", f"{current_press.min:.1f} hPa"
)
col3.metric(
    f"Màxima {hour_str(current_press.max_time)}", f"{current_press.max:.1f} hPa"
)

plotter.pressure_line_plot()

wind = current_wind(data)
st.header(f"Vent - {wind.direction_str} - {wind.name()}")

col1, col2, col3 = st.columns(3)
col1.metric("Direcció", f"{wind.direction_deg} º")
col2.metric("Velocitat", f"10 km/h")
col3.metric("Velocitat màxima", f"30 km/h")

plotter.windspeed_line_plot()

st.sidebar.markdown("# MeteoBeguda")
refresh = st.sidebar.button("Refresca")

st.sidebar.markdown(f"Darrera actualització: {data.timestamp.max()}")

st.sidebar.markdown("## Notícia i agraïments")
st.sidebar.markdown(
    "Aquestes dades reflecteixen l'estat de la meteorologia en temps real a La Beguda Alta (Anoia; vegeu-ne la [wiki](https://ca.wikipedia.org/wiki/La_Beguda_Alta) i [ubicació](https://goo.gl/maps/bXLjN2ScLFrgbRor9))."
)

st.sidebar.markdown(
    "L'origen de les dades és a la web [meteobeguda.cat](http://www.meteobeguda.cat), gestionada per Narcís Batlle, a qui n'agraïm la cessió desinteressada."
)

if refresh:
    load_live.clear()
