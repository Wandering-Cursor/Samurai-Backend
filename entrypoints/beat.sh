mkdir -p /logs

cd DiplomaPulse
celery -A DiplomaPulse beat --loglevel=info