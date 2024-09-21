import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def get_str_conn() -> str:
    username = os.getenv("TIMESCALE_USERNAME")
    password = os.getenv("TIMESCALE_PASSWORD")
    host = os.getenv("TIMESCALE_HOST")
    port = os.getenv("TIMESCALE_PORT")
    dbname = os.getenv("TIMESCALE_DBNAME")
    str_conn = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
    return str_conn


def read_data():
    with create_engine(get_str_conn()).connect() as conn:
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
    return df


def write_forecasts_df(df: pd.DataFrame):
    with create_engine(get_str_conn()).connect() as conn:
        df.to_sql("forecasts", conn, if_exists="append", index=False)


if __name__ == "__main__":
    df = read_data()
    print(df.head())
