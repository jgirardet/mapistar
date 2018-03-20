# Third Party Libraries
# from apistar.permissions import IsAuthenticated
# from config.get_env import env
# from users.authentication import MapistarJWTAuthentication

# AUTHENTICATION = [
#     MapistarJWTAuthentication(),
# ]
# PERMISSIONS = [
#     IsAuthenticated(),
# ]
# JWT = {'SECRET': env['JWT_SECRET'], 'PAYLOAD_DURATION': {'seconds': 300}}

import os

# PONY = {
#     'DATABASE': {
#         'provider': os.environ['DB_ENGINE'],
#         'port': os.environ['DB_PORT'],
#         'database': os.environ['DB_NAME'],
#         'host': os.environ['DB_HOST'],
#         'user': os.environ['DB_USER'],
#         'password': os.environ['DB_PASSWORD'],
#     },
#     'PROJECT_NAME': "mapistar",
#     'INSTALLED_APPS': ["patients"]
# }
PONY = {
    'DATABASE': {
        'provider': os.environ['DB_ENGINE'],
        'port': os.environ['DB_PORT'],
        'database': os.environ['DB_NAME'],
        'host': os.environ['DB_HOST'],
        'user': os.environ['DB_USER'],
        'password': os.environ['DB_PASSWORD'],
    },
    'PROJECT_NAME': "mapistar",
    'INSTALLED_APPS': ["patients"]
}

ACTES_URL = '/actes'

if not ACTES_URL:
    raise Exception(' ACTES_URL not set')
