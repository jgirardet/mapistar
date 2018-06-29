import hug

# import patients
from mapistar import db
from mapistar.db import patients
from pony.orm import db_session

# from mapistar.base_db import api

# from base_db import api
from .auth import IsAuthenticated, JsonWebToken


class PonyMiddleware(object):
    def __init__(self):
        pass

    def process_request(self, request, response):
        """Logs the basic endpoint requested"""
        db_session.__enter__()

    def process_response(self, request, response, resource):
        db_session.__exit__()


def token_verify(token):
    # secret_key = 'super-secret-key-please-change'
    # try:
    #     return jwt.decode(token, secret_key, algorithm='HS256')
    # except jwt.DecodeError:
    #     return False
    return True


api = hug.API(__name__)
api.http.add_middleware(PonyMiddleware())


test_settings = {
    "user_id": "id",
    "user_name": "username",
    "algorithms": ["HS256"],
    "options": {},
    "secret": "aa",
    "white_list": [],
}

Jweb = JsonWebToken(test_settings)

api.http.add_middleware(IsAuthenticated(Jweb))


token_key_authentication = hug.authentication.token(token_verify)
# api.http(requires=token_key_authentication)


# @hug.extend_api()
# def with_other_apis():
#     return [part_1, part_2]


hug.API(__name__).extend(patients, "/patients")
