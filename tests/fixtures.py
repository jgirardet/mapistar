# Standard Libraries
# import json
from unittest.mock import MagicMock

# # Third Party Libraries
import pytest

# from apistar.test import TestClient

# from mapistar.actes.ordo_items import Item
# from mapistar.actes.ordonnances import Ordonnance

# # from mapistar.app import app
from mapistar import User

# from tests import factory
# from mapistar.documents import Document
# from mapistar.first_run import create_directory_tree
# import pathlib


# @pytest.fixture(scope="function")
# def ent():
#     return MagicMock(**{"dico": {"le": "dico"}})


# @pytest.fixture(scope="function")
# def mordo():
#     return MagicMock(spec=Ordonnance)


# @pytest.fixture(scope="function")
# def mitem(ent):
#     return MagicMock(spec=Item, return_value=ent)


@pytest.fixture(scope="function")
def muser(request):
    return MagicMock(spec=User)


# @pytest.fixture(scope="function")
# def mdocu():
#     return MagicMock(spec=Document)


# @pytest.fixture(scope="function")
# def patient():
#     """ patient """
#     return factory.patientf()


# @pytest.fixture(scope="function")
# def user(request):
#     return factory.userf()


# @pytest.fixture(scope="function")
# def acte(request):
#     return factory.actef()


# # @pytest.fixture(scope="function")
# # def observation(request):
# #     return factory.observationf()


# @pytest.fixture(scope="function")
# def ordonnance(request):
#     return factory.ordonnancef()


# # @pytest.fixture(scope="function")
# # def item(request):
# #     return factory.itemf()


# @pytest.fixture(scope="function")
# def arbo(tmpdir):
#     create_directory_tree(tmpdir)
#     return pathlib.Path(tmpdir)


import hug

import pendulum
from functools import partial
from falcon import HTTP_METHODS
from hug.test import call
from mapistar import main
from mapistar.directives import JBB


class Cli:
    def __init__(self, headers={}):
        self.headers = headers
        for method in HTTP_METHODS:
            tester = partial(call, method, main, headers=headers)
            tester.__doc__ = """Simulates a round-trip HTTP {0} against the given API / URL""".format(
                method.upper()
            )
            setattr(self, method.lower(), tester)


@pytest.fixture(scope="module")
def cli_anonymous():
    return Cli()


@pytest.fixture(scope="module")
def clij():
    """
    Permisssions:
        del_patient
    """
    headers = {
        "Authorization": "Bearer "
        + JBB.encode(
            payload={
                "id": 1,
                "username": "j",
                "iat": pendulum.now(),
                "exp": pendulum.now() + pendulum.Duration(seconds=1000),
            }
        )
    }

    return Cli(headers=headers)


@pytest.fixture(scope="module")
def clik():

    headers = {
        "Authorization": "Bearer "
        + JBB.encode(
            payload={
                "id": 2,
                "username": "k",
                "iat": pendulum.now(),
                "exp": pendulum.now() + pendulum.Duration(seconds=1000),
            }
        )
    }

    return Cli(headers=headers)


#     cli = TestClient(app)
#     r = cli.post(
#         app.reverse_url("users:login"),
#         data=json.dumps({"username": "k", "password": "j"}),
#     )
#     token = r.content.decode()
#     cli.headers.update({"Authorization": f"Bearer {token}"})
#     return cli


# @pytest.fixture(scope="module")
# def clil():
#     "admin fixture"
#     cli = TestClient(app)
#     r = cli.post(
#         app.reverse_url("users:login"),
#         data=json.dumps({"username": "l", "password": "j"}),
#     )
#     token = r.content.decode()
#     cli.headers.update({"Authorization": f"Bearer {token}"})
#     return cli
