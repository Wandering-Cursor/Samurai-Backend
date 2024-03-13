#!/bin/bash
set -e -x

docker compose -f compose/db_redis-docker-compose.yml up -d