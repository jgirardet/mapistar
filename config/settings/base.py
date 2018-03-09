# Third Party Libraries
from apistar.permissions import IsAuthenticated
from config.get_env import env
from users.authentication import MapistarJWTAuthentication

AUTHENTICATION = [
    MapistarJWTAuthentication(),
]
PERMISSIONS = [
    IsAuthenticated(),
]
JWT = {'SECRET': env['JWT_SECRET'], 'PAYLOAD_DURATION': {'seconds': 300}}

ACTES_URL = '/actes'

if not ACTES_URL:
    raise Exception(' ACTES_URL not set')
