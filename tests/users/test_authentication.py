# Standard Libraries
from unittest.mock import MagicMock

# Third Party Libraries
import pytest
from apistar.exceptions import BadRequest, Forbidden
from apistar_jwt.exceptions import AuthenticationFailed
from apistar_jwt.token import JWT
from app import settings

from users.authentication import MapistarJWTAuthentication
from users.utils import get_payload


def testautheticate_pass_with_valid_jwt(user, ss):
    valid_jwt = JWT.encode(
        get_payload(user, {'seconds': 8}), settings['JWT']['SECRET'])
    header = "Bearer " + valid_jwt
    engine = MapistarJWTAuthentication()
    authed = engine.authenticate(header, settings, ss)
    assert authed.user == user


def test_authenticate_fails_without_valid_date_payload(user, ss):
    perimed_jwt = JWT.encode(
        get_payload(user, {'seconds': -8}), settings['JWT']['SECRET'])
    header = "Bearer " + perimed_jwt
    engine = MapistarJWTAuthentication()
    with pytest.raises(AuthenticationFailed):
        engine.authenticate(header, settings, ss)


def test_invalid_user(ss):
    a = MagicMock()
    a.id = 35135135135151
    valid_jwt = JWT.encode(
        get_payload(a, {'seconds': 8}), settings['JWT']['SECRET'])
    header = "Bearer " + valid_jwt
    engine = MapistarJWTAuthentication()
    with pytest.raises(BadRequest):
        engine.authenticate(header, settings, ss)


def test_user_is_not_active(user, ss):
    valid_jwt = JWT.encode(
        get_payload(user, {'seconds': 8}), settings['JWT']['SECRET'])
    header = "Bearer " + valid_jwt
    user.is_active = False
    user.save()
    engine = MapistarJWTAuthentication()
    with pytest.raises(Forbidden):
        engine.authenticate(header, settings, ss)


def test_payload_returned_is_empty(user, ss, monkeypatch):
    def return_empty_dict(*args):
        a = MagicMock()
        a.payload = {}
        return a

    monkeypatch.setattr('users.authentication.get_jwt', return_empty_dict)
    valid_jwt = JWT.encode(
        get_payload(user, {'seconds': 8}), settings['JWT']['SECRET'])
    header = "Bearer " + valid_jwt

    engine = MapistarJWTAuthentication()
    with pytest.raises(AuthenticationFailed):
        engine.authenticate(header, settings, ss)


# Test AuthUser
def test_is_authenticated_is_True(auth_user):
    assert auth_user.is_authenticated() == True


def test_get_user_id(auth_user):
    assert auth_user.user.id == auth_user.get_user_id()


def test_get_display_name(auth_user):
    assert auth_user.user.username == auth_user.get_display_name()
