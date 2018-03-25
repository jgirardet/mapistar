import pytest

pytestmark = pytest.mark.pony
from datetime import datetime
from .conftest import patientd, userd
from datetime import datetime
from pony import orm
from mapistar.models import db
import json


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
        print(r.content)
        assert r.status_code == 201