# Standard Libraries
import typing
from contextlib import contextmanager

# Third Party Libraries
import factory
import pytest
from apistar import Component, TestClient
from apistar.backends.django_orm import DjangoORM, Session
from apistar.frameworks.wsgi import WSGIApp as App
from apistar_jwt.token import JWT
from app import components, settings
from config.urls import routes
from tests.factories import *
from users.authentication import AuthUser
from users.models import User
from users.utils import get_payload

################################################
#APISTAR tools
################################################


@pytest.fixture
def ss(db):
    """
    session from django backend
    may be passed as parameter for testing views with session as argument
    """

    # def get_session(backend: DjangoORM,
    #                 ss) -> typing.Generator[Session, None, None]:
    #     print(dir(ss))
    #     yield ss

    return Session(DjangoORM(settings))


@contextmanager
def get_ss(backend: DjangoORM) -> typing.Generator[Session, None, None]:
    yield Session(backend)


@pytest.fixture(scope='session')
def app_fix():
    """
    fixture for apistar app
    Juste mock get_session to get_ss to disable db stuff from apistar
    Use all regular routes and componements of app.py
    All
    """
    comp = []
    for c in components:
        if c.cls is Session:
            c = Component(Session, init=get_ss, preload=False)
        comp.append(c)
    return App(routes=routes, settings=settings, components=comp)


@pytest.fixture
def user(db):
    # a = User.objects.create(username="someone", password="something")
    return User.objects.create(username="someone", password="something")


@pytest.fixture
def auth_user(user):
    return AuthUser(user)


@pytest.fixture
def client(user):
    """
    Authenticated client
    """
    SECRET = settings['JWT'].get('SECRET')

    token = JWT.encode(get_payload(user, {'seconds': 60}), secret=SECRET)
    c = TestClient(app_fix())
    c.headers['Authorization'] = "Bearer " + token
    return c


@pytest.fixture(scope='session')
def client_anonymous(app_fix):
    """
    Anonymous client
    """

    return TestClient(app_fix)


############################################
#models
############################################
"""""" """""" """""" """""" """""" """""" """""" """""" """""
""" """""" """""" """""" """""" """""" """""" """""" """""" ""
# from django.contrib.auth import get_user_model

# from pytest_django.fixtures import db

# User = get_user_model()

# assert 1 == sys.path
"""
PAtients
"""


@pytest.fixture(scope='session')
def patientd():
    """
    just a dict, not saved
    """
    return factory.build(dict, FACTORY_CLASS=FacPatient).copy()


@pytest.fixture
def patient(db):
    """
    return factory mpdele

    """

    return FacPatient()


@pytest.fixture
def patient10(db):
    """
    return 10 patients
    """
    return [FacPatient() for i in range(10)]


# # """
# # actes
# # """


@pytest.fixture(autouse=True, scope='function')
def observation(db):
    """
    fixture for observation instance
    """
    return FacObservation


# #"""
# #Ordonnances
# #""""
# @pytest.fixture(autouse=True)
# def medicamentd(db):
#     return factory.build(
#         dict, FACTORY_CLASS=FacMedicament, ordonnance=FacOrdonnance()).copy()
