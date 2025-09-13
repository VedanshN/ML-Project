"""
Django settings for your project, configured to use environment variables.
"""

import os
from pathlib import Path
import environ

# Initialize django-environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# --- Core Security Settings ---
# SECRET_KEY is read from the .env file
SECRET_KEY = env('SECRET_KEY')

# DEBUG is read from the .env file and cast to a boolean
DEBUG = env('DEBUG')

# ALLOWED_HOSTS is read from the .env file as a comma-separated list
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# --- Application Definitions ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'accounts',
    'uploads',
    'services',
]


# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  #CHANGE THIS TO YOUR FRONTEND URL
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# --- URL Configuration ---
ROOT_URLCONF = 'irs.urls' 


# --- Templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# --- WSGI Application ---
WSGI_APPLICATION = 'irs.wsgi.application' # <-- CHANGE 'your_project_name'


# --- Database Configuration ---
# The DATABASE_URL is parsed automatically by django-environ
DATABASES = {
    'default': env.db('DATABASE_URL')
}


AUTH_USER_MODEL = 'accounts.User'

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True




# --- Default Primary Key Field Type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Email Configuration ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')


# --- Custom App Settings ---
# You can add your own settings from the .env file here
OPENAI_API_KEY = env('OPENAI_API_KEY')