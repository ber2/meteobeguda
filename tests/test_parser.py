import pytest

import pandas as pd

from meteobeguda.parser import COLUMNS, parse_response, parse_timestamps


@pytest.fixture
def raw_input():
    with open("tests/resources/downld02.txt", "rb") as fp:
        raw = fp.read()
    return raw


@pytest.fixture
def parsed_df(raw_input):
    return parse_response(raw_input)


def test_parse_response_has_all_columns(parsed_df):
    assert parsed_df.shape[1] == 29


def test_parsed_response_column_names(parsed_df):
    assert parsed_df.columns.to_list() == list(COLUMNS.keys())


def test_numerical_columns_are_inferred(parsed_df):
    expected_dtypes = pd.Series(COLUMNS.values(), index=COLUMNS.keys())
    pd.testing.assert_series_equal(expected_dtypes, parsed_df.dtypes)


def test_temperatures_are_ordered(parsed_df):
    mask = (parsed_df.temperature_min <= parsed_df.temperature) & (
        parsed_df.temperature <= parsed_df.temperature_max
    )
    assert parsed_df[~mask].shape[0] == 0


def test_windspeed_max_is_higher_than_windspeed(parsed_df):
    mask = parsed_df.windspeed <= parsed_df.windspeed_max
    assert parsed_df[~mask].shape[0] == 0


@pytest.fixture
def parsed_timestamps():
    input_data = {
        "date": ["5/03/2022", "11/03/2022", "9/2/1985"],
        "time": ["18:00", "19:00", "06:30"],
    }
    df = pd.DataFrame(input_data)
    parse_timestamps(df)
    return df


def test_timestamps_are_properly_parsed(parsed_timestamps):
    expected_timestamps = pd.Series(
        [
            pd.Timestamp("2022-03-05 18:00:00"),
            pd.Timestamp("2022-03-11 19:00:00"),
            pd.Timestamp("1985-02-09 06:30:00"),
        ],
        name="timestamp",
    )
    pd.testing.assert_series_equal(expected_timestamps, parsed_timestamps["timestamp"])


@pytest.mark.parametrize("column_name", ["date", "time"])
def test_old_datetime_column_is_dropped_after_parsing_timestamps(
    column_name, parsed_timestamps
):
    assert column_name not in parsed_timestamps.columns


@pytest.fixture
def parsed_df_with_timestamps(parsed_df):
    parse_timestamps(parsed_df)
    return parsed_df


def test_final_df_has_enough_rows(parsed_df_with_timestamps):
    assert parsed_df_with_timestamps.shape[0] == 155


def test_final_df_has_columns(parsed_df_with_timestamps):
    assert parsed_df_with_timestamps.shape[1] == 28


def test_final_df_min_timestamp(parsed_df_with_timestamps):
    assert parsed_df_with_timestamps.timestamp.min() == pd.Timestamp(
        "2022-03-11 00:15:00"
    )


def test_final_df_max_timestamp(parsed_df_with_timestamps):
    assert parsed_df_with_timestamps.timestamp.max() == pd.Timestamp(
        "2022-03-12 14:45:00"
    )
