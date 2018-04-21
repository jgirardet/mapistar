# Standard Libraries
import json
import pytest
from apistar import exceptions

# mapistar


pytestmark = pytest.mark.pony


class TestModel:

    def test_create_user(self, user):
        assert user.id

    def test_repr(self, user):
        assert repr(user) == f"[User: {user.prenom} {user.nom}]"

    def test_check(self, user):
        assert user.check_password("j")


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
            r = cli.post(
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


class TestIsAuthenticated:

    def test_no_header(self, cli_anonymous, app):
        r = cli_anonymous.get(app.reverse_url("patients:liste"))
        assert r.status_code == 401
        assert r.json() == "Authorization header is missing."

    def test_bad_jwt(self, cli, app):
        head = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLmIq4o8Q"}
        r = cli.get(app.reverse_url("patients:liste"), headers=head)
        assert r.json() == "Incorrect authentication credentials."

    def test_pass(self, cli, app, user):
        r = cli.post(
            app.reverse_url("users:login"),
            data=json.dumps({"username": user.username, "password": "j"}),
        )
        token = r.content.decode()
        head = {"Authorization": f"Bearer {token}"}
        r = cli.get(app.reverse_url("patients:liste"), headers=head)
        assert r.status_code == 200
