# Standard Libraries
import json

# Third Party Libraries
import pytest
from apistar import exceptions

pytestmark = pytest.mark.pony
from mapistar.users import User, login


class TestModel:

    def test_create_user(self, mocker):
        m = mocker.patch("mapistar.users.db", return_value="user")
        p = mocker.patch(
            "mapistar.users.generate_password_hash", return_value="pwdcode"
        )

        m.User = mocker.Mock(spec=User, return_value="user")

        m.create_user = User.create_user

        u = m.create_user("user", "pwd", "nom", "prenom")

        p.assert_called_with("pwd")
        m.User.assert_called_with(
            username="user", password="pwdcode", nom="nom", prenom="prenom", actif=True
        )
        assert u == "user"

    def test_repr(self, mocker):
        """
        test autoput of str
        """
        m = mocker.Mock(**{"nom": "nom", "prenom": "prenom"})
        m.__repr__ = User.__repr__
        assert repr(m) == "[User: prenom nom]"

    def test_check(self, mocker):
        p = mocker.patch("mapistar.users.check_password_hash", return_value=True)
        m = mocker.Mock(**{"password": "pwd1"})
        a = User.check_password(m, "pwd2")
        p.assert_called_with(m.password, "pwd2")


from unittest.mock import MagicMock

cred = MagicMock()
cred["username"] = "a"
cred["password"] = "b"

userm = MagicMock(spec=User)


class TestLogin:

    def test_bad_username(self, mocker):
        mocker.patch.object(User, "get", return_value=None)
        with pytest.raises(exceptions.Forbidden) as exc:
            login(cred, "jwt")
        assert str(exc.value) == "Incorrect username or password."

    def test_bad_pwd(self, mocker):
        mocker.patch.object(User, "get", return_value=userm)
        userm.password = "bad pwd"
        userm.check_password.return_value = False
        with pytest.raises(exceptions.Forbidden) as exc:
            login(cred, "jwt")
        assert str(exc.value) == "Incorrect username or password."

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
