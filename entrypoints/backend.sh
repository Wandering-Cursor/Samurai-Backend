#!/bin/bash
set -x  # Enable debugging output
cd DiplomaPulse

echo "Starting backend server..."

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

DEBUG=$(grep -oP '(?<=DEBUG=).*' ../.env | tr -d '\r')

echo "DEBUG=$DEBUG"

if [ "$DEBUG" = "True" ]; then
    echo "Starting backend server in debug mode..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "Starting backend server in production mode..."
    gunicorn DiplomaPulse.wsgi:application --bind 0.0.0.0:8000
fi
