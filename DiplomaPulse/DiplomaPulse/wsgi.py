"""
WSGI config for DiplomaPulse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

from decouple import config
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    config(
        "DJANGO_SETTINGS_MODULE",
        default="DiplomaPulse.settings",
    ),
)

application = get_wsgi_application()
