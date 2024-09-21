CREATE TABLE forecasts (
  symbol TEXT NOT NULL,
  price_type TEXT NOT NULL,
  date TIMESTAMPTZ NOT NULL,
  forecast DOUBLE PRECISION NOT NULL
);
