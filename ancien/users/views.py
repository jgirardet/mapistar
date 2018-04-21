# Third Party Libraries
from apistar import Response, Settings, annotate
from apistar.exceptions import Forbidden
from apistar_jwt.token import JWT
from django.contrib.auth import authenticate

from .utils import get_payload


# login should be unauthenticated
@annotate(authentication=[], permissions=[])
def login(user: str, pwd: str, settings: Settings) -> Response:

    user_logged = authenticate(username=user, password=pwd)
    if not user_logged:
        raise Forbidden("Utilisateur inactif, mauvais login/mot de passe")

    SECRET = settings['JWT'].get('SECRET')

    payload = get_payload(user_logged, settings['JWT'].get('PAYLOAD_DURATION'))

    token = JWT.encode(payload, secret=SECRET)

    return Response({'token': token}, status=201)
