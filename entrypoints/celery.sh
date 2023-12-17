mkdir -p /logs

cd DiplomaPulse
celery -A DiplomaPulse worker --loglevel=info