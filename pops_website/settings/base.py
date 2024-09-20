import os
import json
import logging.config

from dotenv import load_dotenv

load_dotenv("local.env")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# RECAPTCHA SECRET KEY (FOR GOOGLE RECAPTCHA SECURITY)
GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")
GOOGLE_RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")

# # SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", False) == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1").split(",")

# Application definition

INSTALLED_APPS = [
    "crispy_forms",
    "widget_tweaks",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "rest_framework",
    "channels",
    "storages",
    "users.apps.UsersConfig",
    "pops.apps.PopsConfig",
    "team.apps.TeamConfig",
    "chat",
    "debug_toolbar",
]

CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "pops_website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.normpath(os.path.join(BASE_DIR, "templates")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "pops_website.context_processors.mapbox_key",
            ],
        },
    },
]

WSGI_APPLICATION = "pops_website.wsgi.application"
ASGI_APPLICATION = "pops_website.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.getenv("REDIS_SERVER_NAME"), os.getenv("REDIS_PORT"))],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE", "sqlite3"),
        "NAME": os.getenv("DATABASE_NAME", "pops"),
        "USER": os.getenv("DATABASE_USERNAME", "myprojectuser"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "password"),
        "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
        "PORT": os.getenv("DATABASE_PORT", 5432),
        "OPTIONS": json.loads(os.getenv("DATABASE_OPTIONS", "{}")),
    }
}
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# Moving static assets to DigitalOcean Spaces as per:
# https://www.digitalocean.com/community/tutorials/how-to-set-up-object-storage-with-django
USE_S3 = os.getenv("USE_S3")

if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv("STATIC_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("STATIC_SECRET_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("STATIC_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("STATIC_ENDPOINT_URL")
    AWS_S3_CUSTOM_DOMAIN = os.getenv("STATIC_CDN_ENDPOINT_URL")
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    AWS_LOCATION = "static"
    AWS_DEFAULT_ACL = "public-read"
    STATIC_URL = "{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    STATIC_ROOT = "static/"
    STATICFILES_STORAGE = "pops_website.custom_storages.StaticStorage"
    DEFAULT_FILE_STORAGE = "pops_website.custom_storages.MediaStorage"
    MEDIA_URL = "{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, "media/")
    MEDIA_ROOT = "media/"
else:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")


STATICFILES_DIRS = (os.path.join(BASE_DIR, "static_custom"),)

UPLOAD_ROOT = "media/uploads/"

DOWNLOAD_ROOT = os.path.join(PROJECT_ROOT, "static/media/downloads")
DOWNLOAD_URL = STATIC_URL + "media/downloads"

CASE_STUDY_UPLOAD_FILE_TYPES = ["image/tiff"]
CASE_STUDY_UPLOAD_FILE_MAX_SIZE = 209715200  # Max file size in Bytes (multiply KB by 1024, or MB by 1024*1024 to get bytes)

DATA_UPLOAD_MAX_MEMORY_SIZE = 209715200

FILE_UPLOAD_MAX_MEMORY_SIZE = 209715200

# INTERNAL_IPS = os.getenv("INTERNAL_IPS")

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ]
}

CSRF_TRUSTED_ORIGINS = ["https://*.pops-model.org", "https://*.127.0.0.1"]

ADMIN_URL = os.getenv("ADMIN_URL")

AUTH_USER_MODEL = "users.CustomUser"

LOGIN_REDIRECT_URL = "workspace"
LOGOUT_REDIRECT_URL = "/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]
SERVER_EMAIL = os.environ["SERVER_EMAIL"]
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = os.environ["EMAIL_PORT"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"]


# Use this for including the full url in links without access to request
# WEBSITE_URL = "https://popsmodel.org"

# Logging Configuration
# Clear prev config
LOGGING_CONFIG = None

# Get loglevel from env
LOGLEVEL = os.getenv("DJANGO_LOGLEVEL", "info").upper()

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
        },
        "loggers": {
            "": {
                "level": LOGLEVEL,
                "handlers": [
                    "console",
                ],
            },
        },
    }
)

MAPBOX_KEY = os.getenv("MAPBOX_KEY")
# MAPBOX_DASHBOARD_STYLE = os.getenv("MAPBOX_DASHBOARD_STYLE")