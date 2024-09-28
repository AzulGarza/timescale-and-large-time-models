CREATE TABLE stocks_real_time_twelvedata (
  time TIMESTAMPTZ NOT NULL,
  symbol TEXT NOT NULL,
  price DOUBLE PRECISION NULL,
  day_volume INT NULL
);
SELECT create_hypertable('stocks_real_time_twelvedata', by_range('time'));
CREATE INDEX ix_symbol_time_twelvedata ON stocks_real_time_twelvedata (symbol, time DESC);
