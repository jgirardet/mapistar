# Third Party Libraries
import pytest

# from . import factory
from unittest.mock import MagicMock
from mapistar.actes.ordonnances import Ordonnance
from mapistar.actes.ordo_items import Item
from tests import factory


@pytest.fixture(scope="function")
def mordo():
    return MagicMock(spec=Ordonnance)


@pytest.fixture(scope="function")
def mitem():
    return MagicMock(spec=Item)


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


# @pytest.fixture(scope="function")
# def medicament(request):
#     return factory.medicamentf()
from apistar.test import TestClient
from mapistar.app import app
import json


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
