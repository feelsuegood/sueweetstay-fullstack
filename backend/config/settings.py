"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import environ
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# environ.Env.read_env(f"{BASE_DIR}/.env") <- can make a typo mistake
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# create a new secret key
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = env("SECRET_KEY")
GH_ID = env("GH_ID")
GH_SECRET = env("GH_SECRET")
KAKAO_ID = env("KAKAO_ID")
CF_TOKEN = env("CF_TOKEN")
CF_ID = env("CF_ID")

# SECURITY WARNING: don't run with debug turned on in production!
# If there is no RENDER environment variable or If DEBUG is set to True in your .env
# DEBUG => True
DEBUG = ("RENDER" not in os.environ) or (os.getenv("DEBUG", "False") == "True")

if DEBUG:
    ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0", "localhost"]
else:
    ALLOWED_HOSTS = [
        "backend.sueweetstay.com",
        "sueweetstay.com",
        "www.sueweetstay.com",
    ]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "strawberry.django",
    "corsheaders",
]

CUSTOM_APPS = [
    "common.apps.CommonConfig",
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "experiences.apps.ExperiencesConfig",
    "categories.apps.CategoriesConfig",
    "reviews.apps.ReviewsConfig",
    "wishlists.apps.WishlistsConfig",
    "bookings.apps.BookingsConfig",
    "medias.apps.MediasConfig",
    "direct_messages.apps.DirectMessagesConfig",
]

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
        )
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = "en-au"

TIME_ZONE = "Australia/Brisbane"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth

AUTH_USER_MODEL = "users.User"

if DEBUG:
    # allow JS to fetch
    CORS_ALLOWED_ORIGINS = [
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
        "http://localhost:3000",
    ]
    # allow post request from frontend
    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
        "http://localhost:3000",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "https://sueweetstay.com",
        "https://www.sueweetstay.com",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://sueweetstay.com",
        "https://www.sueweetstay.com",
    ]

# allow JS' cookies
CORS_ALLOW_CREDENTIALS = True


MEDIA_ROOT = "uploads"

# just for a url purpose
MEDIA_URL = "user-uploads/"

PAGE_SIZE = 3

# * other third party authentication packages (django-rest-knox (token), Simple JWT)
# https://www.django-rest-framework.org/api-guide/authentication/#third-party-packages
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "config.authentication.TrustMeMateAuthentication",
        "rest_framework.authentication.TokenAuthentication",  # saved in database, force logout available
        "config.authentication.JWTAuthentication",  # not saved in database, can't force logout
    ]
}


def before_send(event, hint):
    if "exc_info" in hint:
        exc_type, exc_value, tb = hint["exc_info"]
        if isinstance(exc_value, SystemExit):  # SIGTERM often occurs as SystemExit
            return None  # Don't send to Sentry
        # ignore RuntimeError related to lifespan
        if isinstance(exc_value, RuntimeError) and str(exc_value).startswith(
            "Django can only handle ASGI/HTTP connections"
        ):
            return None
    return event  # Send the rest of the events


if not DEBUG:
    SESSION_COOKIE_DOMAIN = ".sueweetstay.com"
    CSRF_COOKIE_DOMAIN = ".sueweetstay.com"
    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        integrations=[DjangoIntegration()],
        before_send=before_send,
    )
