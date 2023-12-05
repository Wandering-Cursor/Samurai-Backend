cd DiplomaPulse

python manage.py makemigrations
python manage.py migrate

gunicorn DiplomaPulse.wsgi:application --bind 0.0.0.0:8000