# Third Party Libraries
import jwt
import pendulum
import pytest
from apistar import Client, test

# mapistar
from simple_settings import settings
from mapistar.app import app as main_app

from .factory import *
from .fixtures import *


@pytest.fixture(scope="session")
def cli_anonymous(request):
    """apistar test client"""

    return test.TestClient(main_app)


@pytest.fixture(scope="function")
def cli(user):
    user.flush()
    payload = {
        "id": user.id,
        "username": user.username,
        "iat": pendulum.now(),
        "exp": pendulum.now() + pendulum.Duration(seconds=10),
    }
    token = jwt.encode(payload, key=settings.JWT["JWT_SECRET"]).decode()

    client = test.TestClient(main_app)
    client.headers.update({"Authorization": f"Bearer {token}"})
    client.user = user
    return client


@pytest.fixture(scope="session")
def app(request):
    return main_app
