import pandas as pd

from src.__main__ import read_data, write_forecasts_df


def test_read_data():
    df = read_data()
    assert df is not None
    assert len(df) > 0
    assert df.columns.tolist() == ["symbol", "date", "price_type", "price"]


def test_write_forecasts_df():
    len_fcst_df = 10
    df = pd.DataFrame(
        {
            "symbol": len_fcst_df * ["test_by_azul"],
            "price_type": len_fcst_df * ["close"],
            "date": pd.date_range("2022-01-01", periods=len_fcst_df, freq="D"),
            "forecast": range(len_fcst_df),
        }
    )
    write_forecasts_df(df)
