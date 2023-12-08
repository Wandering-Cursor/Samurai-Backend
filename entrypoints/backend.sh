#!/bin/bash
set -x  # Enable debugging output
set -e  # Stop if any error occurs
cd DiplomaPulse

echo "Starting backend server..."

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

chown -r $USER ./

DEBUG=$(grep -oP '(?<=DEBUG=).*' ../.env | tr -d '\r')

echo "DEBUG=$DEBUG"

if [ "$DEBUG" = "True" ]; then
    echo "Starting backend server in debug mode..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "Starting backend server in production mode..."
    gunicorn --certfile=$CERTFILE_PATH --keyfile=$KEYFILE_PATH DiplomaPulse.wsgi:application --bind 0.0.0.0:443
fi
