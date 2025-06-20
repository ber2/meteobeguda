import datetime as dt
from unittest import mock

import pytest
from meteobeguda.plots import Plotter


@pytest.fixture
def plotter(eight_days):
    return Plotter(eight_days)


def test_plotter_initialization(eight_days):
    plotter = Plotter(eight_days)
    assert plotter.df is eight_days


@mock.patch("streamlit.plotly_chart")
def test_temperature_line_plot(mock_plotly_chart, plotter):
    plotter.temperature_line_plot()

    fig = mock_plotly_chart.call_args[0][0]
    assert fig.data[0].type == "scatter"
    assert fig.data[0].x.shape == (747,)
    assert fig.layout.yaxis.range == (-5.0, 45.0)
    assert fig.layout.yaxis.title.text == "Temperatura (C)"


@mock.patch("streamlit.plotly_chart")
def test_humidity_line_plot(mock_plotly_chart, plotter):
    plotter.humidity_line_plot()

    fig = mock_plotly_chart.call_args[0][0]
    assert fig.data[0].type == "scatter"
    assert fig.data[0].x.shape == (747,)
    assert fig.layout.yaxis.range == (0.0, 100.0)
    assert fig.layout.yaxis.title.text == "Humitat (%)"


@mock.patch("streamlit.plotly_chart")
def test_pressure_line_plot(mock_plotly_chart, plotter):
    plotter.pressure_line_plot()

    fig = mock_plotly_chart.call_args[0][0]
    assert fig.data[0].type == "scatter"
    assert fig.data[0].x.shape == (747,)
    assert fig.layout.yaxis.range == (980.0, 1030.0)
    assert fig.layout.yaxis.title.text == "Pressió atmosfèrica (hPa)"


@mock.patch("streamlit.plotly_chart")
def test_windspeed_line_plot(mock_plotly_chart, plotter):
    plotter.windspeed_line_plot()

    fig = mock_plotly_chart.call_args[0][0]
    assert fig.data[0].type == "scatter"
    assert fig.data[0].x.shape == (747,)
    # assert fig.data[0].x.name == "timestamp"
    # assert fig.data[0].y.name == "windspeed_max"
    assert fig.layout.yaxis.title.text == "Velocitat màxima del vent"


@mock.patch("streamlit.plotly_chart")
def test_rain_hourly_bar_plot(mock_plotly_chart, plotter):
    date = dt.date(2024, 1, 1)
    plotter.rain_hourly_bar_plot(date=date)

    fig = mock_plotly_chart.call_args[0][0]
    assert fig.data[0].type == "bar"
    assert fig.layout.title.text == "Pluja per hora"
    assert fig.layout.yaxis.title.text == "Pluja (mm)"


@mock.patch("streamlit.plotly_chart")
def test_rain_daily_bar_plot(mock_plotly_chart, plotter):
    plotter.rain_daily_bar_plot()

    fig = mock_plotly_chart.call_args[0][0]
    assert fig.data[0].type == "bar"
    assert "Pluja per dia" in fig.layout.title.text


@mock.patch("streamlit.plotly_chart")
def test_temperature_daily_line_plot(mock_plotly_chart, plotter):
    plotter.temperature_daily_line_plot()
    fig = mock_plotly_chart.call_args[0][0]
    assert fig.data[0].type == "scatter"
    assert fig.layout.title.text == "Temperatures diàries"
    assert fig.layout.yaxis.title.text == "Temperatura"
    assert fig.layout.yaxis.range == (-5.0, 45.0)
    assert fig.layout.showlegend is False


@mock.patch("streamlit.plotly_chart")
def test_humidity_daily_line_plot(mock_plotly_chart, plotter):
    plotter.humidity_daily_line_plot()
    fig = mock_plotly_chart.call_args[0][0]
    assert fig.data[0].type == "scatter"
    assert fig.layout.title.text == "Humitat diària"
    assert fig.layout.yaxis.title.text == "Humitat (%)"
    assert fig.layout.yaxis.range == (0.0, 100.0)
    assert fig.layout.showlegend is False


@mock.patch("streamlit.plotly_chart")
def test_pressure_daily_line_plot(mock_plotly_chart, plotter):
    plotter.pressure_daily_line_plot()
    fig = mock_plotly_chart.call_args[0][0]
    assert fig.data[0].type == "scatter"
    assert fig.layout.title.text == "Pressió atmosfèrica diària"
    assert fig.layout.yaxis.title.text == "Pressió (hPa)"
    assert fig.layout.yaxis.range == (980.0, 1030.0)
    assert fig.layout.showlegend is False


@mock.patch("streamlit.plotly_chart")
def test_windspeed_daily_line_plot(mock_plotly_chart, plotter):
    plotter.windspeed_daily_line_plot()
    fig = mock_plotly_chart.call_args[0][0]
    assert fig.data[0].type == "scatter"
    assert fig.layout.title.text == "Velocitat màxima del vent diària"
    assert fig.layout.yaxis.title.text == "Velocitat (km/h)"
    assert fig.layout.showlegend is False
