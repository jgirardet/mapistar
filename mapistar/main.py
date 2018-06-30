import hug

# import patients
from mapistar import db

# from mapistar.db import patients
from pony.orm import db_session

# from mapistar.base_db import api

# from base_db import api
from mapistar.auth import IsAuthenticated, JsonWebToken

from mapistar import directives


class PonyMiddleware(object):
    def __init__(self):
        pass

    def process_request(self, request, response):
        """Logs the basic endpoint requested"""
        db_session.__enter__()

    def process_response(self, request, response, resource):
        db_session.__exit__()


test_settings = {
    "user_id": "id",
    "user_name": "username",
    "algorithms": ["HS256"],
    "options": {},
    "secret": "aa",
    "white_list": ["/", "users/login"],
}


api = hug.API(__name__)


# hug.defaults.directives["jwtoken"] = jwtoken
# jwtoken.directive = True
# from hug.directives import _built_in_directive


# hug.directives["hug_jwtoken"] = jwtoken

# print(api.directives())


api.http.add_middleware(PonyMiddleware())
api.http.add_middleware(IsAuthenticated(directives.JBB))


# hug.API(__name__).extend(rien, "/rien")
hug.API(__name__).extend(db.modules["patients"], "/patients")
hug.API(__name__).extend(db.modules["users"], "/users")
