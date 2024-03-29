"""
Django settings for kursinis project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages
from decouple import config
#config = Config()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True #!!!!!!

ALLOWED_HOSTS =  [config('ALLOWED_HOSTS')]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'sslserver',
    'auth_system',
    'file_system',
    'corsheaders',
]

MIDDLEWARE = [
    'csp.middleware.CSPMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'sslserver.middleware.SSLRedirectMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django_auto_logout.middleware.auto_logout',
]

#forcing https
#SECURE_SSL_REDIRECT = True
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


ROOT_URLCONF = 'kursinis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'kursinis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_kursinis',
        'USER': 'root',
        'PASSWORD': config('PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Vilnius'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'Login'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CSRF_TRUSTED_ORIGINS = [config('ALLOWED_HOSTS_HTTP')]

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
}

#EMAIL CONFIRMATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
EMAIL_PORT = 587 
EMAIL_USE_TLS = True
PASSWORD_RESET_TIMEOUT = 900


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {
            'max_similarity': 0.6,
            'user_attributes': ("username", "email")
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 9,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

#FILE LIMITS
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800 #50mb, kol kas. galima kurti didesnius zemelapiu rinkinius ir tuo paciu nevirsija pythonaywhere uploadatonce limito

#Click-jacking prevencija (didzioji dalis narsykliu i si header reaguoja atitinkamai, t.y. neleidzia puslapiui uzsikrauni frame elemente)
X_FRAME_OPTIONS = 'DENY'

#sausainiuku sifravimas
SESSION_COOKIE_SECURE = True

#automatinis atjungimas po 10 minuciu
AUTO_LOGOUT = {
    'IDLE_TIME':600, 
    'MESSAGE': 'Pasibaige sesijos laikas, junkites is naujo.',
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
    }


CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
  config('ALLOWED_HOSTS_HTTP')
)

#apsauga nuo XSS, CSP konfiguracija
CSP_DEFAULT_SRC = ("'self'",)

CSP_SCRIPT_SRC = (
    "'self'",
    "https://code.jquery.com",
    "https://maxcdn.bootstrapcdn.com",
    "https://ajax.googleapis.com",
    "https://unpkg.com",
    "https://tile.openstreetmap.org",
    "'unsafe-eval'",
)

CSP_STYLE_SRC = (
    "'self'",
    "https://maxcdn.bootstrapcdn.com",
    "https://unpkg.com",
    "https://tile.openstreetmap.org",
    "'unsafe-eval'",
)

CSP_IMG_SRC = (
    "'self'",
    "https://tile.openstreetmap.org",
    "https://unpkg.com",
    "http://127.0.0.2:443",
    "'unsafe-inline'",
    #"data:",
)

CSP_FONT_SRC = ("https://maxcdn.bootstrapcdn.com",)

CSP_SCRIPT_SRC += ("'unsafe-inline'",)
CSP_STYLE_SRC += ("'unsafe-inline'",)