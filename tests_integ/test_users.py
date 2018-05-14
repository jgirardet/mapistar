# Standard Libraries
import json

# Third Party Libraries
import pytest
from apistar import exceptions

pytestmark = pytest.mark.pony
from mapistar.users import User


class TestLogin:

    def test_raise_auth_failed(self, cli, app, user):
        r = cli.post(
            app.reverse_url("users:login"),
            data=json.dumps({"username": user.username, "password": "notthegoodone"}),
        )
        assert r.status_code == 403
        r = cli.post(
            app.reverse_url("users:login"),
            data=json.dumps({"username": "mkmokmokmok", "password": "notthegoodone"}),
        )
        assert r.status_code == 403

    def test_login_pass(self, cli, app, user):
        r = cli.post(
            app.reverse_url("users:login"),
            # "/users/login/",
            data=json.dumps({"username": user.username, "password": "j"}),
        )
        assert r.status_code == 200

    def test_fail_token_none(self, ponydb, monkeypatch, cli, app):
        monkeypatch.setattr("apistar_jwt.token._JWT.encode", lambda x, y: None)
        u = ponydb.User.create_user("j", "j", "j", "j")
        with pytest.raises(exceptions.ConfigurationError) as exc:
            cli.post(
                app.reverse_url("users:login"),
                data=json.dumps({"username": u.username, "password": "j"}),
            )
        assert str(exc.value) == "échec de l'encodage jwt"

    def test_fail_user_inactive(self, ponydb, cli, app):
        u = ponydb.User.create_user("j", "j", "j", "j")
        u.actif = False
        ponydb.commit()
        r = cli.post(
            app.reverse_url("users:login"),
            data=json.dumps({"username": u.username, "password": "j"}),
        )
        assert r.json() == "Utilisateur inactif"

    @pytest.mark.parametrize("login,pwd", [("k", "j"), ("j", "k")])
    def test_fail_bad_user_or_pasword(self, login, pwd, ponydb, cli, app, user):
        u = ponydb.User.create_user("j", "j", "j", "j")
        u.actif = False
        ponydb.commit()
        r = cli.post(
            app.reverse_url("users:login"),
            data=json.dumps({"username": login, "password": pwd}),
        )
        assert r.json() == "Incorrect username or password."
