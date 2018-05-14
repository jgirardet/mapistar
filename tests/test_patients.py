# Standard Libraries
import json
from string import capwords

# Third Party Libraries
import pytest
from pony import orm
from mapistar import patients

from mapistar.patients import db, Patient, PatientCreateSchema, PatientUpdateSchema
from tests.factory import patientf

attrs = ("name", "firstname")


@pytest.mark.pony
class TestPatientModel:

    def test_repr(self, mocker):
        """
        test autoput of str
        """
        m = mocker.Mock(**{"nom": "nom", "prenom": "prenom"})
        m.__repr__ = Patient.__repr__

        assert repr(m) == "[Patient: prenom nom]"

    def test_fields_with_capwords_at_create(self, ponydb):
        """
        must be caps words :
            name
            firstname
        """
        d = {"nom": "ZEFZEF", "prenom": "SDFSDF", "ddn": "1234-12-12", "sexe": "m"}
        a = ponydb.Patient(**d)
        a.flush()
        for i in ["nom", "prenom"]:
            d[i] = capwords(d[i])
        assert a.nom == d["nom"]
        assert a.prenom == d["prenom"]

    def test_fileds_with_capwords_at_update(self, patient):
        patient.nom = "FZEFZEFZEFEZF"
        patient.prenom = "sdfsdfdfsdfsdf sdfsdfsdf"
        patient.flush()
        assert patient.nom == "Fzefzefzefezf"
        assert patient.prenom == "Sdfsdfdfsdfsdf Sdfsdfsdf"


class TestPatientViews:

    def test_add(self, mocker):
        m = mocker.patch.object(db, "Patient", return_value=mocker.Mock(**{"dico": 1}))
        p = PatientCreateSchema(
            **{
                "nom": "Mokmomokok",
                "prenom": "Ljlijjlj",
                "ddn": "1234-12-12",
                "sexe": "m",
            }
        )
        r = patients.add(p)
        assert r.content.decode() == "1"

    def test_cli_get_patient(self, mocker):

        mocker.patch(
            "mapistar.patients.get_or_404", return_value=mocker.Mock(**{"dico": 1})
        )
        r = patients.one(patient_id=1)
        assert r == 1

    def test_cli_del_patient(self, mocker):
        m = mocker.patch("mapistar.patients.get_or_404")
        r = patients.delete(patient_id=1)

        m.return_value.delete.assert_called_once()
        assert r == {"msg": "delete success"}

    def test_cli_list_patient(self, mocker):
        m = mocker.Mock(**{"dico": 1})
        a = [m, m]
        mocker.patch.object(db.Patient, "select", return_value=a)
        r = patients.liste()

        assert r == [1, 1]

    def test_patient_update(self, mocker):
        u = mocker.Mock(**{"dico": 1})
        m = mocker.patch("mapistar.patients.get_or_404", return_value=u)
        p = PatientUpdateSchema(
            **{"prenom": "omkmok", "ddn": "1237-03-03", "rue": "mokmokmok"}
        )
        r = patients.update(new_data=p, patient_id=1)

        m.assert_called_with(db.Patient, 1)
        u.set.assert_called_once_with(
            prenom="omkmok", ddn="1237-03-03", rue="mokmokmok"
        )
        assert r.status_code == 201
