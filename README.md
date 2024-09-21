# timescale and large time models 
> how to integrate large time models into timescale database 

## setup & environment

this template is designed to streamline the setup of any python project. follow these steps to get started:

### 1. install [`uv`](https://github.com/astral-sh/uv/)

use `uv` to manage your virtual environments:

```bash
pip install uv
```

### 2. create a virtual environment

create an environment using python 3.10 (or your preferred version):

```bash
uv venv --python 3.10
```

### 3. activate the environment

activate the virtual environment:

```bash
source .venv/bin/activate
```

### 4. install dependencies

install all the required dependencies from the `requirements.txt` file:

```bash
uv pip install -e .
```

### 5. install pre-commits

```bash
pre-commit install
```

## set up timescale

this process follows the [timescale documentation](https://docs.timescale.com/tutorials/latest/energy-data/dataset-energy/)

1. create a service on [timescale](https://console.cloud.timescale.com/) 
1. save your credentials in the psql config file `~/.pg_service.conf` 
1. download the data and populate timescale using

```bash
make populate_timescale project_id=<your project id>
```

> [!TIP]
> when you create a timescale service, you can download the psql config file.
> also, you will be provided with a psql command such ass `psql -d <your project id>`.
> that's your project id.