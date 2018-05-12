# Standard Libraries
import json
from datetime import datetime

# Third Party Libraries
import pytest
from pony.orm import OperationWithDeletedObjectError

from .factory import observationf, actef

pytestmark = pytest.mark.pony
from mapistar.actes.actes import Acte


class TestActeModel:

    # def test_create_update_date(self, acte, ponydb, patient):
    #     # assert isinstance(acte.created, datetime)
    #     assert acte.modified == acte.created
    #     acte.patient = patient
    #     acte.flush()
    #     assert acte.modified >= acte.created

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

    def test_set_updatable(self, acte):
        with pytest.raises(AttributeError) as e:
            acte.set(**{"_created": datetime.utcnow()})
        assert str(e.value) == "_created n'est pas updatable"
        acte.updatable = ("_created")
        e = datetime.now()
        acte.set(**{"created": e})
        assert acte.to_dict()["created"] == e


# def test_date_modified(self, acte, patient):
#     acte.patient = patient
#     acte.flush()


class TestViews:

    def test_add(self, patient, cli, app):
        a = {"patient": patient.id, "motif": "omk", "body": "mkmok"}
        r = cli.post(app.reverse_url("observations:add"), data=json.dumps(a))
        assert r.status_code == 201

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
