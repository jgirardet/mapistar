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
        'DB_ENGINE': typesystem.string(default=''),
        'DB_PORT': typesystem.string(default=None),
        'DB_NAME': typesystem.string(default=''),
        'DB_HOST': typesystem.string(default=''),
        'DB_USER': typesystem.string(default=''),
        'DB_PASSWORD': typesystem.string(default=''),
        'SECRET_KEY': typesystem.string(default='please_change_it'),
        'JWT_SECRET': typesystem.string(default='please_change_it'),
        'DEBUG': typesystem.boolean(default=True),
        'TEST_RUNNING': typesystem.boolean(default=False)
    }


env = Env()

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.settings')
# if not apps.ready:
#     print("aaaaaaaaaaaaa", settings.configured)
#     settings.configure()
#     django.setup()
