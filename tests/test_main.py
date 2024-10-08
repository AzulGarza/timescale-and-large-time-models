import pandas as pd
from sqlalchemy import text

from forecast.__main__ import (
    forecasting_pipeline,
    read_data_from_timescale,
    timescale_conn,
    write_forecasts_to_timescale,
)


def test_read_data():
    with timescale_conn() as conn:
        df = read_data_from_timescale(conn)
    assert df is not None
    assert len(df) > 0
    assert df.columns.tolist() == ["unique_id", "date", "price"]


def test_write_forecasts_df():
    len_fcst_df = 10
    df = pd.DataFrame(
        {
            "unique_id": len_fcst_df * ["test_by_azul__close"],
            "date": pd.date_range("2022-01-01", periods=len_fcst_df, freq="D"),
            "TimeGPT": range(len_fcst_df),
        }
    )
    with timescale_conn() as conn:
        write_forecasts_to_timescale(conn, df)
        df = pd.read_sql_query(
            """
            SELECT * FROM forecasts WHERE symbol = 'test_by_azul'
            """,
            conn,
        )
        assert len(df) == len_fcst_df
        conn.execute(text("DELETE FROM forecasts WHERE symbol = 'test_by_azul'"))
        conn.commit()


def test_forecasting_pipeline():
    forecasting_pipeline(10)
