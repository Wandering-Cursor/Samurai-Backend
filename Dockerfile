FROM python:3.12

WORKDIR /app

COPY pyproject.toml pdm.lock README.md /app/

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY ./src /app/src
COPY static/ /app/static

RUN pdm sync --prod --no-editable
