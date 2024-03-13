FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml pdm.lock README.md /app/
COPY samurai/ /app/samurai/

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

WORKDIR /app

RUN pip install -U pip setuptools wheel
RUN pip install pdm

RUN pdm sync --prod --no-editable

COPY entrypoints/ /app/entrypoints/
RUN chmod +x /app/entrypoints/*.sh
COPY .env /app/

USER appuser
