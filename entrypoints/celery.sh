#!/bin/bash
set -e -x
echo "Starting celery worker"

pdm run_celery_worker

echo "Exited!!!"