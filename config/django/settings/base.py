# Third Party Libraries
from config.get_env import env

DJANGO_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = []

SECRET_KEY = env['SECRET_KEY']

LOCAL_APPS = [
    'patients',
    'users',
    'actes',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# change default user
AUTH_USER_MODEL = 'users.User'

USE_TZ = True

TIME_ZONE = "Europe/Paris"
