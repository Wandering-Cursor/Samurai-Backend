FROM python:3.12

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

COPY . /app/

RUN chmod +x /app/*.sh /app/entrypoints/*sh

EXPOSE 8000

ENTRYPOINT [ "bash", "/app/entrypoints/backend.sh" ]