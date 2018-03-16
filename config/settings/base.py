# Third Party Libraries
# from apistar.permissions import IsAuthenticated
from config.get_env import env
# from users.authentication import MapistarJWTAuthentication

# AUTHENTICATION = [
#     MapistarJWTAuthentication(),
# ]
# PERMISSIONS = [
#     IsAuthenticated(),
# ]
JWT = {'SECRET': env['JWT_SECRET'], 'PAYLOAD_DURATION': {'seconds': 300}}

PONY = {
    'DATABASE': {
        'provider': env['DB_ENGINE'],
        'port': env['DB_PORT'],
        'database': env['DB_NAME'],
        'host': env['DB_HOST'],
        'user': env['DB_USER'],
        'password': env['DB_PASSWORD'],
    },
    'PROJECT_NAME': "mapistar",
    'INSTALLED_APPS': ["patients"]
}

ACTES_URL = '/actes'

if not ACTES_URL:
    raise Exception(' ACTES_URL not set')
