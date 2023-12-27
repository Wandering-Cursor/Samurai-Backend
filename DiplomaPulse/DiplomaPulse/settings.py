from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
	"ALLOWED_HOSTS",
	default=[],
	cast=lambda v: [s.strip() for s in v.split(",")],
)
CSRF_TRUSTED_ORIGINS = config(
	"CSRF_TRUSTED_ORIGINS",
	default=[],
	cast=lambda v: [s.strip() for s in v.split(",")],
)

CORS_ALLOWED_ORIGINS = config(
	"CORS_ALLOWED_ORIGINS",
	default=[],
	cast=lambda v: [s.strip() for s in v.split(",")],
)

STATIC_ROOT = config("STATIC_ROOT", default=f"{BASE_DIR}/staticfiles")
MEDIA_ROOT = config("MEDIA_ROOT", default=f"{BASE_DIR}/media")

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
]

internal_apps = [
	"core",
	"accounts",
	"administration",
	"communication",
	"students",
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
]

if DEBUG:
	CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "DiplomaPulse.urls"

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

WSGI_APPLICATION = "DiplomaPulse.wsgi.application"


DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql",
		"NAME": config("DB_NAME"),
		"USER": config("DB_USER"),
		"PASSWORD": config("DB_PASSWORD", default=""),
		"HOST": config("DB_HOST"),
		"PORT": config("DB_PORT"),
	}
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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Django REST Framework

REST_FRAMEWORK = {
	"DEFAULT_AUTHENTICATION_CLASSES": (
		"rest_framework_simplejwt.authentication.JWTAuthentication",
	),
}

# Swagger (drf_yasg) settings

SWAGGER_SETTINGS = {
	"USE_SESSION_AUTH": False,
	"SECURITY_DEFINITIONS": {
		"Token": {"type": "apiKey", "name": "Authorization", "in": "header"},
	},
}

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
		"default": {
			"level": "INFO",
			"class": "logging.handlers.RotatingFileHandler",
			"filename": "/logs/django.log",
			"formatter": "app",
			"maxBytes": 1024 * 1024 * 10,
			"backupCount": 10,
		},
		"request_handler": {
			"level": "INFO",
			"class": "logging.handlers.RotatingFileHandler",
			"filename": "/logs/django_request.log",
			"formatter": "app",
			"maxBytes": 1024 * 1024 * 10,
			"backupCount": 10,
		},
	},
	"loggers": {
		"django": {"handlers": ["default"], "level": "INFO", "propagate": True},
		"django.request": {"handlers": ["request_handler"], "level": "DEBUG", "propagate": True},
	},
	"root": {"level": "INFO", "handlers": ["default"]},
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.BaseUser"
