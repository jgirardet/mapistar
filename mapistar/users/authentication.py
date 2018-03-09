# Third Party Libraries
from apistar import Settings, http
from apistar.backends.django_orm import Session as Db
from apistar.exceptions import BadRequest, Forbidden
from apistar.interfaces import Auth
from apistar_jwt.authentication import get_jwt
from apistar_jwt.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


class AuthUser(Auth):

    def __init__(self, user: get_user_model(), token=None):
        # def __init__(self, user, token=None):
        self.user = user
        self.token = token

    def is_authenticated(self) -> bool:
        return True

    def get_display_name(self) -> str:
        return self.user.username

    def get_user_id(self) -> str:
        return self.user.id


class MapistarJWTAuthentication():
    def authenticate(self, authorization: http.Header, settings: Settings, db: Db):
        # Firs we check token validity
        jwt = get_jwt(authorization, settings)
        if jwt.payload == {}:
            raise AuthenticationFailed("payload non validé")

        # Get User instance
        user_id = jwt.payload['user_id']
        try:
            user = db.User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise BadRequest('User in token not found')

        if not user.is_active:
            raise Forbidden("User Inactive")
        return AuthUser(user=user)
