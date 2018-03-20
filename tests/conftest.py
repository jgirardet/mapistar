import pytest
from .factory import *
from app import app as main_app
from apistar import test


@pytest.fixture(scope='session')
def cli(request):
    """apistar test client"""
    return test.TestClient(main_app)


@pytest.fixture(scope='session')
def app(request):
    return main_app