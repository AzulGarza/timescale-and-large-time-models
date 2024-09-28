import os
from contextlib import contextmanager
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from nixtla import NixtlaClient
from sqlalchemy import create_engine

load_dotenv()


@contextmanager
def timescale_conn():
    username = os.getenv("TIMESCALE_USERNAME")
    password = os.getenv("TIMESCALE_PASSWORD")
    host = os.getenv("TIMESCALE_HOST")
    port = os.getenv("TIMESCALE_PORT")
    dbname = os.getenv("TIMESCALE_DBNAME")
    str_conn = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(str_conn)
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()
        engine.dispose()


def read_data_from_timescale(conn: Any, table: str = "one_day_candle"):
    df = pd.read_sql_query(
        f"""
        SELECT symbol, bucket as date, open, high, low, close
        FROM {table} 
        ORDER BY symbol, bucket DESC
        LIMIT 100
        """,
        conn,
    )
    df = df.melt(
        id_vars=["symbol", "date"],
        var_name="price_type",
        value_name="price",
    )
    df["unique_id"] = df["symbol"] + "__" + df["price_type"].astype(str)
    return df[["unique_id", "date", "price"]]


def write_forecasts_to_timescale(conn: Any, df: pd.DataFrame, table: str = "forecasts"):
    df = df.rename(columns={"TimeGPT": "forecast"})
    df[["symbol", "price_type"]] = df["unique_id"].str.split("__", expand=True)
    df = df.drop(columns="unique_id")
    df.to_sql(table, conn, if_exists="append", index=False)


def _forecasting_pipeline(
    conn: Any,
    h: int,
    freq: str,
    add_fcd: bool,
    read_table: str = "one_day_candle",
    write_table: str = "forecasts",
):
    df = read_data_from_timescale(conn, table=read_table)
    if df.empty:
        raise ValueError("omggg, empty dataframe")
    nixtla = NixtlaClient()
    fcst_df = nixtla.forecast(df, h=h, time_col="date", target_col="price", freq=freq)
    if add_fcd:
        fcst_df["forecast_creation_date"] = pd.Timestamp.now()
    write_forecasts_to_timescale(conn, fcst_df, table=write_table)


def forecasting_pipeline(h: int, freq: str = "D", add_fcd: bool = False):
    with timescale_conn() as conn:
        _forecasting_pipeline(conn, h, freq, add_fcd)


if __name__ == "__main__":
    import fire

    fire.Fire(forecasting_pipeline)
