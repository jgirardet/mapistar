import pytest

from mapistar.auth import JsonWebToken
import pendulum

test_settings = {
    "user_id": "id",
    "user_name": "username",
    "algorithms": ["HS256"],
    "options": {},
    "secret": "aa",
    "white_list": [],
}

payload = {
    "id": 1,
    "username": "hello",
    "iat": pendulum.now(),
    "exp": pendulum.now() + pendulum.Duration(seconds=1000),
}


def test__JWT():
    j = JsonWebToken(test_settings)
    e = j.encode(payload)

    u = j.decode(e)
    assert u.id == 1
    assert u.username == "hello"
