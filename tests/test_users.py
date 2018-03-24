# Third Party Libraries
import pytest


class TestModel:
    def test_create_user(self, user):
        assert user.pk
    def test_repr(self,user):
        assert repr(user) == "[User: Prenom Nom]"
    def test_check(self, user):
        assert user.check_password("j")
