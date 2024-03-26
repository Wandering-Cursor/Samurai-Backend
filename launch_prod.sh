#!/bin/bash
set -e -x

docker build -t samurai-backend-web .
docker compose -f ./compose/docker-docker-compose.yml up -d
