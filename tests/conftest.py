import pytest
import pandas as pd


@pytest.fixture
def eight_days():
    return pd.read_parquet("tests/resources/eight_days.parquet")
