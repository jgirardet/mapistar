# Standard Libraries
import json
from unittest.mock import Mock

# Third Party Libraries
import pytest

# mapistar
# pytestmark = pytest.mark.pony
from mapistar.actes.actes import Acte
from mapistar.actes.views import ActesViews
from mapistar.utils import DicoMixin, NameMixin, SetMixin
from tests.factory import actef


class TestActeModel:
    def test_inheritance(self):
        assert issubclass(Acte, DicoMixin)
        assert issubclass(Acte, SetMixin)
        assert issubclass(Acte, NameMixin)

    def test_before_insert(self, mocker):
        # assert isinstance(acte.created, datetime)
        f = mocker.MagicMock(spec=Acte, **{"created": 1, "modified": None})

        assert f.created is not f.modified
        Acte.before_insert(f)
        assert f.created is f.modified

    def test_before_update(self, mocker):
        f = mocker.MagicMock(spec=Acte, **{"modified": None})
        m = mocker.patch("mapistar.actes.actes.datetime")
        Acte.before_update(f)
        assert m.utcnow.return_value is f.modified


acte = Mock(spec=Acte)
mock_dico = Mock(**{"dico": {"le": "dico"}})
acte.return_value = mock_dico
jwtuser = Mock(**{"id": 12})


class ActeTest(ActesViews):
    model = acte
    schema_add = dict()
    schema_update = dict()


class ActeModele(ActesViews):
    model = Acte


class TestViews:
    def test_add(self, mocker):
        r = ActeTest.add()(data={"patient": 99}, user=jwtuser)
        assert json.loads(r.content) == {"le": "dico"}
        assert r.status_code == 201
        acte.assert_called_with(owner=12, patient=99)

    @pytest.mark.pony
    def test_list_acte_pass(self, patient, user):
        obs = [actef(owner=user.id, patient=patient.id) for i in range(3)]
        # ponydb.flush()
        r = ActeModele.liste()(patient.id)
        assert {x["id"] for x in r} == {x.id for x in obs}

    def test_one_pass(self, mocker):
        m = Mock()
        r = mocker.patch("mapistar.actes.views.get_or_404", return_value=m)
        t = ActeModele.one()(33)

        r.assert_called_with(Acte, 33)
        assert t == m.dico

    def test_delete_pass(self, mocker):
        r = ActeModele.delete()(35, acte)

        acte.delete.assert_called_once()
        assert r == {"id": 35, "deleted": True}

    def test_update_pass(self, mocker):
        upd = {"modified": "123456"}
        t = ActeModele.update()(47, upd, acte)

        acte.set.assert_called_with(modified="123456")
        assert t == acte.dico
