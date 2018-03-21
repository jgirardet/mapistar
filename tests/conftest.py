# Third Party Libraries
import pytest
from apistar import test
from app import app as main_app

from .factory import *


@pytest.fixture(scope='session')
def cli(request):
    """apistar test client"""
    return test.TestClient(main_app)


@pytest.fixture(scope='session')
def app(request):
    return main_app
