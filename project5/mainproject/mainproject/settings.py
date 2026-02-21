"""
Django settings for mainproject project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ---------------- BASE DIR ---------------- #
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- LOAD .env ---------------- #
load_dotenv(BASE_DIR / ".env")

# ---------------- SECURITY ---------------- #
SECRET_KEY = 'django-insecure-%4!7_r&wv4-iga8!7a0x1d6gp%l7bec$12p#=kyx3ygit^z7^*'

DEBUG = True

ALLOWED_HOSTS = []

# ---------------- API KEYS ---------------- #
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ---------------- APPLICATIONS ---------------- #
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portal',
]

# ---------------- MIDDLEWARE ---------------- #
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------- URLS ---------------- #
ROOT_URLCONF = 'mainproject.urls'

# ---------------- TEMPLATES ---------------- #
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # main templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mainproject.wsgi.application'

# ---------------- DATABASE ---------------- #
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------- PASSWORD VALIDATION ---------------- #
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

# ---------------- INTERNATIONALIZATION ---------------- #
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------- STATIC FILES ---------------- #
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ---------------- LOGIN REDIRECTS ---------------- #
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# ---------------- DEFAULT PRIMARY KEY ---------------- #
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
