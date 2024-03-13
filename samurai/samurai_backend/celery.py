import os

from celery import Celery
from decouple import config
from django.conf import settings

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    config(
        "DJANGO_SETTINGS_MODULE",
        default="samurai_backend.settings.settings",
    ),
)
app = Celery("samurai_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()
