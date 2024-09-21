import os
from contextlib import contextmanager

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


def read_data_from_timescale():
    with timescale_conn() as conn:
        df = pd.read_sql_query(
            """
            SELECT symbol, bucket as date, open, high, low, close
            FROM one_day_candle
            ORDER BY symbol, bucket DESC
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


def write_forecasts_to_timescale(df: pd.DataFrame):
    df = df.rename(columns={"TimeGPT": "forecast"})
    df[["symbol", "price_type"]] = df["unique_id"].str.split("__", expand=True)
    df = df.drop(columns="unique_id")
    with timescale_conn() as conn:
        df.to_sql("forecasts", conn, if_exists="append", index=False)


def forecasting_pipeline(h: int):
    df = read_data_from_timescale()
    nixtla = NixtlaClient()
    fcst_df = nixtla.forecast(df, h=h, time_col="date", target_col="price", freq="D")
    write_forecasts_to_timescale(fcst_df)


if __name__ == "__main__":
    import fire

    fire.Fire(forecasting_pipeline)
