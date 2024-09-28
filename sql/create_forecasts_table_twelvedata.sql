CREATE TABLE forecasts_twelvedata (
  forecast_creation_date TIMESTAMPTZ NOT NULL,
  symbol TEXT NOT NULL,
  price_type TEXT NOT NULL,
  date TIMESTAMPTZ NOT NULL,
  forecast DOUBLE PRECISION NOT NULL
);
