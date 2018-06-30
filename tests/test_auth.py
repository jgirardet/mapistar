from unittest.mock import MagicMock

import falcon
import jwt
import pendulum
import pytest
from mapistar.auth import JsonWebToken, IsAuthenticated
from pony.orm import db_session
from tests.factory import userf

test_settings = {
    "user_id": "id",
    "algorithms": ["HS256"],
    "options": {},
    "secret": "aa",
    "white_list": ["/ble"],
}

payload = {
    "id": 1,
    "username": "hello",
    "iat": pendulum.now(),
    "exp": pendulum.now() + pendulum.Duration(seconds=1000),
}


@pytest.fixture(scope="function")
def fjwt(request):
    return JsonWebToken(test_settings)


# from mapistar import auth


class TestJsonWEbToken:
    def test_init(self):
        a = JsonWebToken(test_settings)
        assert a.ID == "id"
        assert a.algorithms == ["HS256"]
        assert a.options == {}
        assert a.secret == "aa"
        assert a.white_list == ["/ble"]

    def test_encode(self, mocker, fjwt):
        m = mocker.patch("mapistar.auth.jwt.encode")
        fjwt.encode(payload="payload")
        m.assert_called_with("payload", "aa", algorithm="HS256")

    def test_encode_exception(self, mocker, fjwt):
        m = mocker.patch("mapistar.auth.jwt.encode", side_effect=Exception)
        s = mocker.MagicMock(**{"secret": "lp"})
        a = JsonWebToken.encode(s, payload="payload", algorithms="HS256")
        assert a == None

    def test_encode_ok(self, mocker):
        m = mocker.patch("mapistar.auth.jwt.encode", return_value=b"la_token")
        s = mocker.MagicMock(**{"secret": "lp"})
        a = JsonWebToken.encode(s, payload="payload", algorithms="HS256")
        assert a == "la_token"

    def test_decode(self, mocker):
        m = mocker.patch("mapistar.auth.jwt.decode", return_value=None)
        a = JsonWebToken.decode(1, 2)
        assert a == None

        m = mocker.patch(
            "mapistar.auth.jwt.decode", side_effect=jwt.MissingRequiredClaimError
        )
        assert JsonWebToken.decode(1, 2) is None

        m = mocker.patch("mapistar.auth.jwt.decode", side_effect=jwt.InvalidTokenError)
        assert JsonWebToken.decode(1, 2) is None

        m = mocker.patch("mapistar.auth.jwt.decode", side_effect=Exception)
        assert JsonWebToken.decode(1, 2) is None

    def test_decode_ok(self, mocker):
        # good token
        m = mocker.patch("mapistar.auth.User")
        # payload {"id":1}
        token = (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.40ZTiQiy-NdLGZVwpyJdzQso7CjQ8uCizp4M_c4D4FA"
        )
        a = JsonWebToken({"secret": "aa"})
        r = a.decode(token)
        assert r == (m.__getitem__(1), {"id": 1})

    @pytest.mark.parametrize(
        "header,err",
        [
            (None, "Authorization header is missing."),
            ("Bearerzerzerzer", "Could not seperate Authorization scheme and token."),
            ("NOT Bereare", "Authorization scheme not supported, try Bearer"),
        ],
    )
    def test_get_token_fail(self, header, err):
        with pytest.raises(falcon.HTTPUnauthorized) as exc:
            JsonWebToken.get_token_from_header(header)
        assert exc.value.title == err

    def test_get_token_ok(self):
        a = JsonWebToken.get_token_from_header("Bearer azerty")
        assert a == "azerty"


from pony.orm import db_session


class TestIsAuthenticated:
    def test_white_list(self, mocker):
        a = IsAuthenticated(mocker.MagicMock(**{"white_list": ["/white"]}))
        r = mocker.MagicMock(**{"path": "/white"})
        assert a.process_request(r, "response") is None

        r = mocker.MagicMock(
            **{
                "path": "/notwhite",
                "auth": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.40ZTiQiy-NdLGZVwpyJdzQso7CjQ8uCizp4M_c4D4FA",
                "context": {},
            }
        )
        a = IsAuthenticated(JsonWebToken({"secret": "aa"}))
        m = mocker.patch("mapistar.auth.User")

        e = a.process_request(r, "response")
        assert r.context["user"] == m.__getitem__()
        assert r.context["payload"] == {"id": 1}
