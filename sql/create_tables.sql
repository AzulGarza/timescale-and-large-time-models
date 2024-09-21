CREATE TABLE "metrics" (
    created timestamp with time zone default now() not null,
    type_id integer not null,
    value double precision not null
);
SELECT create_hypertable('metrics', 'created');
\COPY metrics FROM 'data/metrics.csv' CSV;
SELECT * FROM metrics LIMIT 5;
