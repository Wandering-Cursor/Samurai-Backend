from __future__ import absolute_import, unicode_literals
from django.conf import settings
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DiplomaPulse.settings")
app = Celery("DiplomaPulse")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()
