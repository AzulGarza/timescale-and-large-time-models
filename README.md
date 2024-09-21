# python-project-template  
> a simple template for organizing any python project.

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

## ready to code  
you're now all set to start building your project.
