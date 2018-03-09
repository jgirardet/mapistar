# Standard Libraries
import pathlib
import sys

# Third Party Libraries
from apistar import environment, typesystem

# import os
# from django.conf import settings
# from django.apps import apps
# import django


class Env(environment.Environment):
    properties = {
        'DB_ENGINE': typesystem.string(default='django.db.backends.sqlite3'),
        'DB_PORT': typesystem.string(default=''),
        'DB_NAME': typesystem.string(default='db.local'),
        'DB_HOST': typesystem.string(default=''),
        'DB_USER': typesystem.string(default=''),
        'DB_PASSWORD': typesystem.string(default=''),
        'SECRET_KEY': typesystem.string(default='please_change_it'),
        'JWT_SECRET': typesystem.string(default='please_change_it'),
        'DEBUG': typesystem.boolean(default=True),
        'TEST_RUNNING': typesystem.boolean(default=False)
    }


env = Env()

# add app folder to sys.path
PROJECT_ROOT = pathlib.Path(__file__).absolute()
PROJECT_ROOT = PROJECT_ROOT.parents[1] / "mapistar"
sys.path.insert(0, str(PROJECT_ROOT))

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.settings')
# if not apps.ready:
#     print("aaaaaaaaaaaaa", settings.configured)
#     settings.configure()
#     django.setup()
