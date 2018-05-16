# Third Party Libraries
# Standard Libraries
# Standard Libraries
# Standard Libraries
# Standard Libraries
# Standard Libraries
# Standard Libraries
import json
# from . import factory
from unittest.mock import MagicMock

import pytest
# @pytest.fixture(scope="function")
# def medicament(request):
#     return factory.medicamentf()
from apistar.test import TestClient
from tests import factory

# mapistar
from mapistar.actes.ordo_items import Item
from mapistar.actes.ordonnances import Ordonnance
from mapistar.app import app


@pytest.fixture(scope="function")
def ent():
    return MagicMock(**{"dico": {"le": "dico"}})


@pytest.fixture(scope="function")
def mordo():
    return MagicMock(spec=Ordonnance)


@pytest.fixture(scope="function")
def mitem(ent):
    return MagicMock(spec=Item, return_value=ent)


@pytest.fixture(scope="function")
def patient():
    """ patient """
    return factory.patientf()


@pytest.fixture(scope="function")
def user(request):
    return factory.userf()


# @pytest.fixture(scope="function")
# def acte(request):
#     return factory.actef()


# @pytest.fixture(scope="function")
# def observation(request):
#     return factory.observationf()


@pytest.fixture(scope="function")
def ordonnance(request):
    return factory.ordonnancef()


# @pytest.fixture(scope="function")
# def item(request):
#     return factory.itemf()




@pytest.fixture(scope="module")
def clij():
    cli = TestClient(app)
    r = cli.post(
        app.reverse_url("users:login"),
        data=json.dumps({"username": "j", "password": "j"}),
    )
    token = r.content.decode()
    cli.headers.update({"Authorization": f"Bearer {token}"})

    return cli


@pytest.fixture(scope="module")
def clik():
    cli = TestClient(app)
    r = cli.post(
        app.reverse_url("users:login"),
        data=json.dumps({"username": "k", "password": "j"}),
    )
    token = r.content.decode()
    cli.headers.update({"Authorization": f"Bearer {token}"})
    return cli
