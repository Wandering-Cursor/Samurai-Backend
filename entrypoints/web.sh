#!/bin/bash
set -e -x
echo "Starting backend server..."

pdm manage makemigrations
pdm manage migrate
pdm run_server

echo "Exited!!!