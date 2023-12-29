import os
from pathlib import Path
from django.contrib.messages import constants

BASE_DIR = Path(__file__).resolve().parent.parent

# Prod
SECRET_KEY = 'django-insecure-wwjs1cqcnr&%w_@p^90gx)_g*^55ai2zh2q-_alfn#ii0n*38l'
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'product',
    'order',
    'profiles',

    # TODO: Remove debug toolbar after the entire project is done
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # TODO: Remove toolbar middleware after the entire project is done
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'hero.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hero.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static/Media files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join('templates/static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Message tags
MESSAGE_TAGS = {
    constants.DEBUG: 'alert-info',
    constants.ERROR: 'alert-danger',
    constants.INFO: 'alert-info',
    constants.SUCCESS: 'alert-success',
    constants.WARNING: 'alert-warning',
}

# Session in days
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7

# Save every request
SESSION_SAVE_EVERY_REQUEST = False

# Serializer - JSON pattern
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# TODO: Remove internal ips after the entire project is done
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
