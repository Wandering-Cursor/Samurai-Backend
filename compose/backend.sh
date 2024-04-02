#!/bin/bash
set -e -x

echo "Activating virtual environment"
source .venv/bin/activate

echo "Running migrations"
cd /app/src/samurai_backend
alembic upgrade head
echo "Migrations complete"

# Return to root directory
cd /app

echo "Add default permissions"
pdm create_permissions
echo "Default permissions added"

echo "Starting backend server"
uvicorn samurai_backend.app:app --proxy-headers --host 0.0.0.0 --port 8000
echo "Backend server exited"
