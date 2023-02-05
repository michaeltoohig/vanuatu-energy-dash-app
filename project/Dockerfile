FROM python:3.10.8-slim-buster

# configure poetry
ENV POETRY_VERSION=1.2.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# set working directory
WORKDIR /usr/src

# set environment varibles
# prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install system dependencies
# apt-get -y install netcat gcc && \
RUN apt-get update && \
    curl -sSL https://install.python-poetry.org | python - && \
    apt-get clean
ENV PATH="${PATH}:/root/.poetry/bin"

# copy poetry dependencies files to parent directory
# so `poetry run` command can be used in workdir
COPY ./pyproject.toml /usr/src/
# install dependencies to container's Python interpreter
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main -E deployment

# copy project files 
COPY app/ /usr/src/app

CMD gunicorn -b 0.0.0.0:8050 app.app:server
