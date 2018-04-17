# Third Party Libraries
import jwt
import pendulum
import pytest
from apistar import Client, test

# mapistar
from app import app as main_app
from mapistar import settings

from .fixtures import *


@pytest.fixture(scope="session")
def cli_anonymous(request):
    """apistar test client"""

    return test.TestClient(main_app)



@pytest.fixture(scope="function")
def cli(user):

    payload = {
        "user": user.pk,
        "username": user.username,
        "iat": pendulum.utcnow(),
        "exp": pendulum.utcnow() + pendulum.Interval(seconds=10),
    }
    token = jwt.encode(payload, key=settings.JWT['JWT_SECRET']).decode()

    client = test.TestClient(main_app)
    client.headers.update({'Authorization': f'Bearer {token}'})
    # import pdb
    # pdb.set_trace()
    return client


@pytest.fixture(scope="session")
def app(request):
    return main_app
