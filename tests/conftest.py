# Third Party Libraries
import pytest
from apistar import Client, test
from app import app as main_app

from .factory import *


@pytest.fixture(scope='session')
def cli(request):
    """apistar test client"""

    return  test.TestClient(main_app)
    
    # t =  test.TestClient(main_app)
    # return Client(document=document, session=t)


@pytest.fixture(scope='session')
def app(request):
    return main_app
