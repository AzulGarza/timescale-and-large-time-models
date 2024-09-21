import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def read_data():
    username = os.getenv("TIMESCALE_USERNAME")
    password = os.getenv("TIMESCALE_PASSWORD")
    host = os.getenv("TIMESCALE_HOST")
    port = os.getenv("TIMESCALE_PORT")
    dbname = os.getenv("TIMESCALE_DBNAME")
    CONNECTION = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    with psycopg2.connect(CONNECTION) as conn:
        df = pd.read_sql_query(
            """
            SELECT symbol, bucket as date, open, high, low, close
            FROM one_day_candle
            ORDER BY symbol, bucket DESC
            """,
            conn,
        )
    return df


if __name__ == "__main__":
    df = read_data()
    print(df.head())
