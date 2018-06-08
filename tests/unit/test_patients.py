# Standard Libraries


# mapistar
from mapistar import patients
from mapistar.patients import Patient, PatientCreateSchema, PatientUpdateSchema, db

attrs = ("name", "firstname")


class TestPatientModel:
    def test_capswords(self, mocker):
        a = mocker.Mock(**{"prenom": "prenom", "nom": "nom"})
        Patient._capwords(a)
        assert a.prenom == "Prenom"
        assert a.nom == "Nom"

    def test_before_insert(self, mocker):
        a = mocker.Mock(**{"prenom": "prenom", "nom": "nom"})
        Patient.before_insert(a)

        a._capwords.assert_called_once()
        assert a.alive is True

    def test_before_update(self, mocker):
        a = mocker.Mock()
        Patient.before_update(a)

        a._capwords.assert_called_once()

    def test_repr(self, mocker):
        """
        test autoput of str
        """
        m = mocker.Mock(**{"nom": "nom", "prenom": "prenom"})
        m.__repr__ = Patient.__repr__

        assert repr(m) == "[Patient: prenom nom]"


class TestPatientViews:
    def test_add(self, mocker):
        mocker.patch.object(db, "Patient", return_value=mocker.Mock(**{"dico": 1}))
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
