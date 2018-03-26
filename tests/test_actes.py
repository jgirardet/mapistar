import pytest

pytestmark = pytest.mark.pony
from datetime import datetime
from .conftest import patientd, userd
from datetime import datetime
from pony import orm
from pony.orm import OperationWithDeletedObjectError
from mapistar.models import db
import json
from .factory import patientd


class TestActeModel:
    def test_create_update_date(self, acte, ponydb):
        assert isinstance(acte.created, datetime)
        assert acte.modified == acte.created
        acte.patient = ponydb.Patient(**patientd())
        acte.flush()
        assert acte.modified >= acte.created

    def test_set(self, acte):
        with pytest.raises(AttributeError) as e:
            acte.set(**{'created': datetime.now()})
        assert str(e.value) == "created n'est pas updatable"
        acte.updatable = ("created")
        e = datetime.now()
        acte.set(**{'created': e})
        assert acte.to_dict()['created'] == e


class TestViews:
    def test_add(self, patient, user, cli, app):
        a = {'patient': patient.pk, 'motif': "omk", "body": "mkmok"}
        r = cli.post(app.reverse_url("observations:add"), data=json.dumps(a))
        assert r.status_code == 201

    def test_list_acte_pass(self, patient, app, cli, user, fk):
        obss = [
            db.Observation(
                patient=patient.pk, owner=user.pk, motif=fk.sentence())
            for i in range(3)
        ]
        fobss = [
            db.Observation(
                patient=db.Patient(**patientd()),
                owner=user.pk,
                motif=fk.sentence()) for i in range(3)
        ]
        r = cli.get(
            app.reverse_url("observations:liste", patient_pk=patient.pk))
        assert {x['pk'] for x in r.json()} == {x.pk for x in obss}

    def test_one_pass(self, observation, cli, app):
        r = cli.get(
            app.reverse_url("observations:one", acte_pk=observation.pk))
        assert r.status_code == 200
        assert r.json() == observation.dico

    def test_delete_pass(self, observation, cli, app):
        r = cli.delete(
            app.reverse_url("observations:delete", acte_pk=observation.pk))
        assert r.status_code == 200
        with pytest.raises(OperationWithDeletedObjectError):
            observation.dico

    def test_update_pass(self, observation, cli, app):
        upd = {"motif": "mokmokmok"}
        r = cli.put(
            app.reverse_url("observations:delete", acte_pk=observation.pk),
            data=json.dumps(upd))
        assert r.status_code == 200
        assert r.json()['motif'] == "mokmokmok"
