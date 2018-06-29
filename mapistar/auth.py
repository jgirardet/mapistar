from falcon import HTTPUnauthorized
import jwt


class JWTUser:
    slots = ("id", "username", "token")

    def __init__(self, id, username, token) -> None:
        self.id = id
        self.username = username
        self.token = token

    def __repr__(self):
        return f"User:[{self.username} {self.id}]"


class JsonWebToken:
    slots = ("ID", "USERNAME", "algorithms", "options", "secret")

    test_settings = {
        "user_id": "id",
        "user_name": "username",
        "algorithms": ["HS256"],
        "options": {},
        "secret": "aa",
        "white_list": [],
    }

    def __init__(self, settings) -> None:
        self.ID = settings.get("user_id")
        self.USERNAME = settings.get("user_name")
        self.algorithms = settings.get("algorithms")
        self.options = settings.get("options")
        self.secret = settings.get("secret")

    def encode(self, payload, algorithm=None, **kwargs) -> str:
        algorithm = algorithm if algorithm else self.algorithms[0]
        try:
            token = jwt.encode(payload, self.secret, algorithm=algorithm).decode(
                encoding="UTF-8"
            )
        except Exception as exc:
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
        username = payload.get(self.USERNAME)
        return JWTUser(id=_id, username=username, token=payload)

    @staticmethod
    def get_token_from_header(headers):
        authorization = headers.get("AUTHORIZATION", None)
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


class IsAuthenticated(object):
    """check all request is"""

    def __init__(self, jwt):
        self.jwt = jwt

    def process_request(self, request, response):
        """Logs the basic endpoint requested"""

        token = self.jwt.get_token_from_header(request.headers)
        user = self.jwt.decode(token)
        request.context["user"] = user
        return user
