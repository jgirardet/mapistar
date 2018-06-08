# Standard Libraries
from unittest.mock import MagicMock

# Third Party Libraries
import pytest
from apistar import exceptions

# mapistar
from mapistar.users import User, login

from werkzeug.security import check_password_hash


class TestModel:
    def test_create_user(self, mocker):
        m = mocker.patch("mapistar.users.db", return_value="user")
        p = mocker.patch(
            "mapistar.users.generate_password_hash", return_value="pwdcode"
        )

        m.User = mocker.Mock(spec=User, return_value="user")

        m.create_user = User.create_user

        u = m.create_user("user", "pwd", "nom", "prenom", "docteur")

        p.assert_called_with("pwd")
        m.User.assert_called_with(
            username="user",
            password="pwdcode",
            nom="nom",
            prenom="prenom",
            statut="docteur",
            actif=True,
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
        User.check_password(m, "pwd2")
        p.assert_called_with(m.password, "pwd2")

    def test_change_password(self, mocker):
        userm = MagicMock(spec=User)

        userm.check_password.return_value = False
        with pytest.raises(exceptions.Forbidden) as exc:
            User.change_password(userm, "old", "new1", "new2")

        userm.check_password.return_value = True
        with pytest.raises(exceptions.Forbidden) as exc:
            User.change_password(userm, "old", "new1", "new2")
        assert str(exc.value) == "Les mots de passes ne correspondent pas"

        User.change_password(userm, "old", "new1", "new1")
        assert check_password_hash(userm.pwd, "new1")


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

    def test_login_pass(self, mocker):
        mocker.patch.object(User, "get", return_value=userm)
        userm.check_password.return_value = True
        jwt = mocker.MagicMock()
        jwt.encode = lambda x: x
        assert {"id", "username", "iat", "exp"} == set(login(cred, jwt).keys())

    def test_fail_token_none(self, mocker):
        mocker.patch.object(User, "get", return_value=userm)
        userm.check_password.return_value = True
        jwt = mocker.MagicMock()
        jwt.encode.return_value = None

        with pytest.raises(exceptions.ConfigurationError) as exc:
            login(cred, jwt)
        assert str(exc.value) == "échec de l'encodage jwt"

    def test_fail_user_inactive(self, mocker):
        mocker.patch.object(User, "get", return_value=userm)
        userm.check_password.return_value = True
        userm.actif = False
        jwt = mocker.MagicMock()
        jwt.encode.return_value = True
        with pytest.raises(exceptions.Forbidden) as exc:
            login(cred, jwt)
        assert str(exc.value) == "Utilisateur inactif"
