# forecasting stock-trade data using timescale and large time models 
> how to integrate large time models into timescale database 

this project demonstrates how to integrate forecasts into a [Timescale database](https://docs.timescale.com/), using [TimeGPT](https://docs.nixtla.io/).

## set up env

```bash
pip install uv
uv venv --python 3.10
source .venv/bin/activate
uv pip install -e .
pre-commit install
```

## set up timescale

> [!TIP]
> when you create a timescale service, you can download the psql config file.
> also, you will be provided with a psql command such ass `psql -d <your project id>`.
> that's your project id.

### finance tutorial part 1: loading and forecasting data on demand

this process follows the [timescale documentation](https://docs.timescale.com/tutorials/latest/financial-tick-data/financial-tick-dataset)

1. create a service on [timescale](https://console.cloud.timescale.com/) 
1. save your credentials in the psql config file `~/.pg_service.conf` 
1. download the data and populate timescale using

```bash
make populate_timescale project_id=<your project id>
make create_materialized_view project_id=<your project id>
make create_forecasts_table project_id=<your project id>
```

1. forecast! 

```bash
python forecast --h <your horizon>
```

### finance tutorial part 2: loading and forecasting real time data

this process follows the [timescale documentation](https://docs.timescale.com/tutorials/latest/financial-ingest-real-time/)

1. create a service on [timescale](https://console.cloud.timescale.com/) 
1. save your credentials in the psql config file `~/.pg_service.conf` 

```bash
make create_twelvedata_table project_id=<your project id>
make create_m_view_twelvedata project_id=<your project id>
make create_f_table_twelvedata project_id=<your project id>
```

1. collect real time data, ingest it to timescale and forecast it in real time! 

```bash
python forecast/real_time.py
```
