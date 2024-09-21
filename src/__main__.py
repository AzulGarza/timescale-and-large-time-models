import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_str_conn() -> str:
    username = os.getenv("TIMESCALE_USERNAME")
    password = os.getenv("TIMESCALE_PASSWORD")
    host = os.getenv("TIMESCALE_HOST")
    port = os.getenv("TIMESCALE_PORT")
    dbname = os.getenv("TIMESCALE_DBNAME")
    str_conn = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    return str_conn


def read_data():
    with psycopg2.connect(get_str_conn()) as conn:
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


if __name__ == "__main__":
    df = read_data()
    print(df.head())
