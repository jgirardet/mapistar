import hug

# import patients
from mapistar import db
from mapistar.db import patients
from pony.orm import db_session

# from mapistar.base_db import api

# from base_db import api


class PonyMiddleware(object):
    """A middleware that logs all incoming requests and outgoing responses that make their way through the API"""

    __slots__ = ("logger",)

    def __init__(self):
        pass

    #     self.logger = logger if logger is not None else logging.getLogger('hug')

    def process_request(self, request, response):
        """Logs the basic endpoint requested"""
        db_session.__enter__()

    def process_response(self, request, response, resource):
        db_session.__exit__()


api = hug.API(__name__)
api.http.add_middleware(PonyMiddleware())


# @hug.extend_api()
# def with_other_apis():
#     return [part_1, part_2]


hug.API(__name__).extend(patients, "/patients")
