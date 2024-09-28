import os
import time
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from twelvedata import TDClient

from forecast.__main__ import _forecasting_pipeline, timescale_conn

load_dotenv()


class WebsocketPipeline:
    DB_TABLE = "stocks_real_time_twelvedata"
    DB_CANDLE = "one_minute_candle_twelvedata"
    DB_FORECASTS = "forecasts_twelvedata"
    DB_COLUMNS = ["time", "symbol", "price", "day_volume"]
    MAX_BATCH_SIZE = 5

    def __init__(self, conn):
        self.conn = conn
        self.current_batch = []
        self.insert_counter = 0

    def _insert_values(self, data):
        if self.conn is not None:
            session = sessionmaker(bind=self.conn)()
            sql = f"""
            INSERT INTO {self.DB_TABLE} ({','.join(self.DB_COLUMNS)})
            VALUES (:value1, :value2, :value3, :value4);"""
            try:
                for row in data:
                    params = {
                        f"value{i+1}": row[i] for i in range(len(self.DB_COLUMNS))
                    }
                    session.execute(text(sql), params)
                session.commit()

            except Exception as e:
                session.rollback()
                print(f"Error inserting data: {e}")

    def _forecast(self):
        try:
            self.conn.execution_options(isolation_level="AUTOCOMMIT").execute(
                text(
                    f"""
        CALL refresh_continuous_aggregate('{self.DB_CANDLE}', NULL, NULL);
                    """
                )
            )
        except Exception as e:
            print(f"Error refreshing aggregates: {e}")
        _forecasting_pipeline(
            self.conn,
            h=5,
            freq="1min",
            add_fcd=True,
            read_table=self.DB_CANDLE,
            write_table=self.DB_FORECASTS,
        )

    def _on_event(self, event):
        if event["event"] == "price":
            timestamp = datetime.utcfromtimestamp(event["timestamp"])
            data = (timestamp, event["symbol"], event["price"], event.get("day_volume"))
            self.current_batch.append(data)
            print(f"Current batch size: {len(self.current_batch)}")
            if len(self.current_batch) == self.MAX_BATCH_SIZE:
                self._insert_values(self.current_batch)
                self.insert_counter += 1
                print(f"Batch insert #{self.insert_counter}")
                self.current_batch = []
                self._forecast()

    def start(self, symbols):
        td = TDClient(apikey=os.getenv("TWELVEDATA_API_KEY"))
        ws = td.websocket(on_event=self._on_event)
        ws.subscribe(symbols)
        ws.connect()
        while True:
            ws.heartbeat()
            time.sleep(10)


if __name__ == "__main__":
    symbols = ["BTC/USD"]
    with timescale_conn() as conn:
        websocket = WebsocketPipeline(conn)
        websocket.start(symbols=symbols)
