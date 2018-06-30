from falcon import HTTPUnauthorized
import jwt
from mapistar import User
from simple_settings import settings


class JsonWebToken:
    __slots__ = ("ID", "algorithms", "options", "secret", "white_list")

    def __init__(self, settings) -> None:
        self.ID = settings.get("user_id", "id")
        self.algorithms = settings.get("algorithms", ["HS256"])
        self.options = settings.get("options", {})
        self.secret = settings.get("secret")
        self.white_list = settings.get("white_list", [])

    def encode(self, payload, algorithm=None, **kwargs) -> str:
        algorithm = algorithm if algorithm else self.algorithms[0]
        try:
            token = jwt.encode(payload, self.secret, algorithm=algorithm).decode(
                encoding="UTF-8"
            )
        except Exception as exc:
            print("erreur de creation du token", exc)
            # log.warn(exc.__class__.__name__)
            return None
        return token

    def decode(self, token):
        try:
            payload = jwt.decode(
                token, self.secret, algorithms=self.algorithms, **self.options
            )
            if payload == {}:
                return None
        except jwt.MissingRequiredClaimError as exc:
            # log.warning("JWT Missing claim: %s", exc.claim)
            return None
        except jwt.InvalidTokenError as exc:
            # log.exception("JWT Invalid Token: %s", exc.__class__.__name__)
            return None
        except Exception as exc:
            # log.exception("JWT Exception: %s", exc.__class__.__name__)
            return None
        _id = payload.get(self.ID)
        return (User[_id], payload)

    @staticmethod
    def get_token_from_header(authorization):
        if authorization is None:
            raise HTTPUnauthorized(title="Authorization header is missing.")
        try:
            scheme, token = authorization.split()
        except ValueError:
            raise HTTPUnauthorized(
                title="Could not seperate Authorization scheme and token."
            )
        if scheme.lower() != "bearer":
            raise HTTPUnauthorized(
                title="Authorization scheme not supported, try Bearer"
            )

        return token


class IsAuthenticated(object):
    """check all request is"""

    def __init__(self, jwt):
        self.jwt = jwt

    def process_request(self, request, response):
        if request.path in self.jwt.white_list:
            return None
        token = self.jwt.get_token_from_header(request.auth)
        request.context["user"], request.context["payload"] = self.jwt.decode(token)


# class JWT:
#     slots = "settings"

#     def __init__(self, settings: Dict = None) -> None:
#         def get(setting, default=None):
#             return settings.get(setting, os.environ.get(setting, default))

#         settings = settings if settings else {}
#         self.settings = {
#             "user_id": get("JWT_USER_ID", "id"),
#             "user_name": get("JWT_USER_NAME", "username"),
#             "algorithms": get("JWT_ALGORITHMS", ["HS256"]),
#             "options": get("JWT_OPTIONS", {}),
#             "secret": get("JWT_SECRET"),
#             "white_list": get("JWT_WHITE_LIST", []),
#         }
#         if self.settings["secret"] is None:
#             self._raise_setup_error()

#     def _raise_setup_error(self):
#         msg = (
#             "JWT_SECRET must be defined as an environment variable or passed as part of"
#             " settings on instantiation."
#             " See https://github.com/audiolion/apistar-jwt#Setup"
#         )
#         raise Exception(msg) #ConfigurationError(msg)

#     def resolve(
#         self, authorization: http.Header, route: Route, parameter: inspect.Parameter
#     ) -> Union[_JWT, JWTUser, None]:
#         authentication_required = getattr(route.handler, "authenticated", True)
#         jwt = _JWT(self.settings)
#         if parameter.annotation is JWT:
#             return jwt
#         if route.handler.__name__ in self.settings["white_list"]:
#             return None
#         if authorization is None and not authentication_required:
#             return None
#         token = get_token_from_header(authorization)
#         jwt_user = jwt.decode(token)
#         if jwt_user is None:
#             raise AuthenticationFailed()


# return jwt_user
# return request.context["user"]
