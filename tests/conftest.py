
import pytest
from apistar import App, test

from mapistar.app import app as main_app, components, routes
from tests.factory import *  # noqa: F403, F401
from tests.fixtures import *  # noqa: F403, F401


@pytest.fixture(scope="session")
def napp(request):
    """ No Auth App; No Db_session"""
    # event_hooks = []
    return App(routes=routes, components=components)


@pytest.fixture(scope="session")
def cli_anonymous(napp):
    """apistar test client"""

    return test.TestClient(main_app)


@pytest.fixture(scope="session")
def cli_app_no_auth(napp):
    """apistar test client"""

    return test.TestClient(main_app)


# test_timer = None
# import time


# def pytest_runtest_setup(item):
#     global test_timer
#     test_timer = time.time()


# def pytest_runtest_teardown(item, nextitem):
#     global test_timer
#     c = time.time() - test_timer
#     print(item.name, int(c * 1000), " ms")
