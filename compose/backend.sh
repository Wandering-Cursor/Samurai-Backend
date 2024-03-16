#!/bin/bash
set -e -x

echo "Activating virtual environment"
source .venv/bin/activate

echo "Starting backend server"
uvicorn samurai_backend.app:app --proxy-headers --host 0.0.0.0 --port 8000
echo "Backend server exited"
