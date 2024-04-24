#!/bin/bash
set -e -x

echo "Info"
pdm show

echo "Running migrations"
cd /app/src/samurai_backend
pdm run alembic upgrade head
echo "Migrations complete"

cd /app

echo "Add default permissions"
pdm create_permissions
echo "Default permissions added"

echo "Starting backend server"
pdm run uvicorn samurai_backend.app:app --proxy-headers --host 0.0.0.0 --port 8000
echo "Backend server exited"
