CREATE TABLE stocks_real_time (
  time TIMESTAMPTZ NOT NULL,
  symbol TEXT NOT NULL,
  price DOUBLE PRECISION NULL,
  day_volume INT NULL
);
SELECT create_hypertable('stocks_real_time', by_range('time'));
CREATE INDEX ix_symbol_time ON stocks_real_time (symbol, time DESC);
CREATE TABLE company (
  symbol TEXT NOT NULL,
  name TEXT NOT NULL
);
\COPY stocks_real_time from './data/tutorial_sample_tick.csv' DELIMITER ',' CSV HEADER;
\COPY company from './data/tutorial_sample_company.csv' DELIMITER ',' CSV HEADER;
