# timescale and large time models 
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

this process follows the [timescale documentation](https://docs.timescale.com/tutorials/latest/financial-tick-data/financial-tick-dataset)

1. create a service on [timescale](https://console.cloud.timescale.com/) 
1. save your credentials in the psql config file `~/.pg_service.conf` 
1. download the data and populate timescale using

```bash
make populate_timescale project_id=<your project id>
make create_materialized_view project_id=<your project id>
make create_forecasts_table project_id=<your project id>
```

> [!TIP]
> when you create a timescale service, you can download the psql config file.
> also, you will be provided with a psql command such ass `psql -d <your project id>`.
> that's your project id.
