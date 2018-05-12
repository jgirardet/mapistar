# Standard Libraries
import json
from datetime import datetime

# Third Party Libraries
import pytest
from pony.orm import OperationWithDeletedObjectError

from .factory import observationf

pytestmark = pytest.mark.pony
from mapistar.actes.actes import Acte
from mapistar.actes.views import ActesViews


class TestActeModel:

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

    def test_set_updatable(self, mocker):
        f = mocker.MagicMock(spec=Acte, **{"created": 1, "updatable": []})
        f.set = Acte.set
        with pytest.raises(AttributeError) as e:
            Acte.set(f, **{"_created": datetime.utcnow()})

        assert str(e.value) == "_created n'est pas updatable"

        f.updatable = ("created",)
        g = mocker.patch("builtins.super")
        h = g.return_value
        Acte.set(f, **{"created": "AAA"})
        mocker.stopall()

        h.set.assert_called_with(created="AAA")


from unittest.mock import Mock

acte = Mock(spec=Acte)
acte.return_value = Mock(**{"dico": {"le": "dico"}})
jwtuser = Mock(**{"id": 12})
import json


class ActeTest(ActesViews):
    model = acte
    schema_add = dict()
    schema_update = dict()


class TestViews:

    def test_add(self, mocker):
        # m = mocker.patch.object(db, "Acte", return_value=mocker.Mock(**{"dico": 1}))
        p = {
            "nom": "Mokmomokok", "prenom": "Ljlijjlj", "ddn": "1234-12-12", "sexe": "m"
        }

        r = ActeTest.add()(data={"patient": 99}, user=jwtuser)
        assert json.loads(r.content) == {"le": "dico"}
        assert r.status_code == 201
        acte.assert_called_with(owner=12, patient=99)

    def test_list_acte_pass(self, patient, app, cli, ponydb):

        obs = [observationf(owner=cli.user, patient=patient) for i in range(3)]
        ponydb.commit()
        r = cli.get(app.reverse_url("observations:liste", patient_id=patient.id))
        assert {x["id"] for x in r.json()} == {x.id for x in obs}

    def test_one_pass(self, observation, cli, app):
        r = cli.get(app.reverse_url("observations:one", acte_id=observation.id))
        assert r.status_code == 200
        assert r.json() == observation.dico

    def test_delete_pass(self, observation, cli, app):
        observation.owner = cli.user
        r = cli.delete(app.reverse_url("observations:delete", acte_id=observation.id))
        assert r.status_code == 200
        with pytest.raises(OperationWithDeletedObjectError):
            observation.dico

    def test_update_pass(self, cli, app, observation):
        observation.owner = cli.user
        upd = {"motif": "mokmokmok"}
        r = cli.put(
            app.reverse_url("observations:update", acte_id=observation.id),
            data=json.dumps(upd),
        )

        assert r.status_code == 200
        assert r.json()["motif"] == "mokmokmok"
