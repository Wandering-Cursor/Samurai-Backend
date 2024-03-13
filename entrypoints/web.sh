#!/bin/bash
set -e -x
echo "Starting backend server..."

pdm run_server

echo "Exited!!!