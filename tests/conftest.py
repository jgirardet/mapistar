# Third Party Libraries
# Standard Libraries
# Standard Libraries
# Standard Libraries
# Standard Libraries
# Standard Libraries
import time

import jwt
import pendulum
import pytest
from apistar import App, test
from simple_settings import settings
from tests.factory import *  # noqa: F403, F401
from tests.fixtures import *  # noqa: F403, F401

# mapistar
from mapistar.app import app as main_app
from mapistar.app import components, routes

# @pytest.fixture(scope="function")
# def cli(user):
#     user.flush()
#     payload = {
#         "id": user.id,
#         "username": user.username,
#         "iat": pendulum.now(),
#         "exp": pendulum.now() + pendulum.Duration(seconds=10),
#     }
#     token = jwt.encode(payload, key=settings.JWT["JWT_SECRET"]).decode()

#     client = test.TestClient(main_app)
#     client.headers.update({"Authorization": f"Bearer {token}"})
#     client.user = user
#     return client


# @pytest.fixture(scope="session")
# def app(request):
#     return main_app


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


# def pytest_sessionstart(session):
#     db_path = session.config.getini("PONY_DB")
#     db = importlib.import_module(db_path).db
#     db.drop_all_tables(with_all_data=True)
#     db.create_tables()
#     generate_db()


# # from mapistar.db import db

# import importlib


# def pytest_sessionfinish(session, exitstatus):
#     db_path = session.config.getini("PONY_DB")
#     db = importlib.import_module(db_path).db
#     db.drop_all_tables(with_all_data=True)



test_timer = None


def pytest_runtest_setup(item):
    global test_timer
    test_timer = time.time()


def pytest_runtest_teardown(item, nextitem):
    global test_timer
    c = time.time() - test_timer
    print(item.name, int(c * 1000), " ms")
