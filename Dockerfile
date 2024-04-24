FROM python:3.12

WORKDIR /app

RUN pip install -U pip setuptools wheel
RUN pip install pdm

ADD pyproject.toml pyproject.toml
ADD pdm.lock pdm.lock
ADD README.md README.md

RUN pdm install --frozen-lockfile --prod --no-editable

ADD compose/backend.sh entrypoint.sh
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

COPY src src
COPY static/ static

ENTRYPOINT [ "bash", "entrypoint.sh" ]
