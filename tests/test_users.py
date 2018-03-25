# Third Party Libraries
import pytest


class TestModel:
    def test_create_user(self, user):
        assert user.pk
    def test_repr(self,user):
        assert repr(user) == f"[User: {user.prenom} {user.nom}]"
    def test_check(self, user):
        assert user.check_password("j")
