import os
from pathlib import Path

import dj_database_url
from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default=[],
    cast=Csv(),
)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default=[],
    cast=Csv(),
)

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default=[],
    cast=Csv(),
)

STATIC_ROOT = config("STATIC_ROOT", default=BASE_DIR / "staticfiles")
MEDIA_ROOT = config("MEDIA_ROOT", default=BASE_DIR / "media")

BASE_URL = config("BASE_URL", default="http://localhost:8000")


# As required by https://django-autocomplete-light.readthedocs.io/en/master/install.html#configuration
# dal and dal_select2 is placed before django.contrib.admin

django_apps = [
    "dal",
    "dal_select2",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
external_apps = [
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
    "oauth2_provider",
]

internal_apps = [
    "core",
    "accounts",
    "administration",
    "communication",
    "students",
    "organization",
]


INSTALLED_APPS = django_apps + internal_apps + external_apps

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "samurai_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "samurai_backend.wsgi.application"


DATABASES = {
    "default": dj_database_url.config(
        env="DB_URL",
    )
}

CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [str(BASE_DIR / "locale")]


# Django REST Framework

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
}

# Swagger (drf_yasg) settings

OAUTH2_PROVIDER = {
    "SCOPES": {"read": "Read scope", "write": "Write scope", "groups": "Access to your groups"}
}

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Your App API - Swagger": {
            "type": "oauth2",
            "authorizationUrl": "/oauth/authorize",
            "tokenUrl": "/oauth/authorize/",
            "flow": "accessCode",
            "scopes": {
                "read groups": "read groups",
            },
        }
    },
    "OAUTH2_REDIRECT_URL": "/static/drf-yasg/swagger-ui-dist/oauth2-redirect.html",
    "OAUTH2_CONFIG": {
        "clientId": "yourAppClientId",
        "clientSecret": "yourAppClientSecret",
        "appName": "your application name",
    },
    "DOC_EXPANSION": "none",
    "DEEP_LINKING": True,
    "SHOW_EXTENSIONS": True,
    "PERSIST_AUTH": True,
}

BASE_LOGS_DIR = Path(config("BASE_LOGS_DIR", default=BASE_DIR / "logs") if DEBUG else "/logs")

os.makedirs(BASE_LOGS_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app": {
            "format": "%(asctime)s [%(levelname)-8s] (%(module)s.%(funcName)s) %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "app",
        },
        "default": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_LOGS_DIR / "django.log",
            "formatter": "app",
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 10,
        },
        "request_handler": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_LOGS_DIR / "django_request.log",
            "formatter": "app",
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 10,
        },
    },
    "loggers": {
        "django": {"handlers": ["console", "default"], "level": "INFO", "propagate": True},
        "django.request": {
            "handlers": ["console", "request_handler"],
            "level": "INFO",
            "propagate": True,
        },
    },
    "root": {"level": "INFO", "handlers": ["console", "default"]},
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AUTH_USER_MODEL = "accounts.BaseUser"
