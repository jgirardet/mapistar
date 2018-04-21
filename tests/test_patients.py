# Standard Libraries
import json
from string import capwords

# Third Party Libraries
import pytest
from pony import orm

pytestmark = pytest.mark.pony

# @pytest.mark.usefixtures('patientd')
attrs = ("name", "firstname")


class TestPatientModel:

    def test_repr(self, ponydb, patient):
        """
        test autoput of str
        """

        assert repr(patient) == f"[Patient: {patient.prenom} {patient.nom}]"

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

    def test_fileds_with_capwords_at_update(self, patient, ponydb):
        patient.nom = "FZEFZEFZEFEZF"
        patient.prenom = "sdfsdfdfsdfsdf sdfsdfsdf"
        orm.commit()
        assert patient.nom == "Fzefzefzefezf"
        assert patient.prenom == "Sdfsdfdfsdfsdf Sdfsdfsdf"


class TestPatientSchema:
    # def test_all_args(self, ponydb):
    #     "all args un create schema are in model Patient"
    #     a = ponydb.Patient(**PatientUpdateSchema({
    #         'nom': "Mokmomokok",
    #         'prenom': "Ljlijjlj",
    #         'ddn': "1234-12-12",
    #         "sexe": "m",
    #         "cp": 21345,
    #         "ville": "kmkokmo",
    #         "tel": "+33645896745",
    #         "email": "dze@zfe.gt",
    #         "alive": False,
    #     }))
    #     assert a
    pass


class TestPatientViews:

    def test_cli_patient_create(self, cli, app):
        a = {
            "nom": "Mokmomokok", "prenom": "Ljlijjlj", "ddn": "1234-12-12", "sexe": "m"
        }

        resp = cli.post(app.reverse_url("patients:add"), data=json.dumps(a))
        assert resp.json()["pk"] is not None

    def test_cli_get_patient(self, patient, cli, app):
        resp = cli.get(app.reverse_url("patients:get", pk=patient.pk))
        assert resp.json() == patient.dico

    def test_cli_del_patient(self, patient, cli, app):
        resp = cli.delete(app.reverse_url("patients:delete", pk=patient.pk))
        assert resp.json() == {"msg": "delete success"}

    def test_cli_list_patient(self, patient, cli, app):
        e = []
        for i in range(5):
            e.append(patient)
        orm.commit()
        resp = cli.get(app.reverse_url("patients:liste"))
        assert {i["nom"] for i in resp.json()} == {i.nom for i in e}

    def test_patient_update(self, patient, cli, app):
        patient.sexe = "m"
        patient.flush()
        update = {"prenom": "omkmok", "ddn": "1237-03-03", "rue": "mokmokmok"}
        response = cli.put(
            app.reverse_url("patients:update", pk=patient.pk), data=json.dumps(update)
        )
        for i in update:
            assert response.json() == patient.dico
        assert response.status_code == 201


# def test_add_Ee(cli):
#     r = cli.post(
#         "/patients/eee/",
#         data=json.dumps(
#             {
#                 "nom": "Mokmomokok",
#                 "prenom": "Ljlijjlj",
#                 # "a": "hello Cerberus",
#                 "ddn": "1234-12-12",
#                 "sexe": "f",
#             }
#         ),
#     )

#     assert r.status_code == 201
#     assert r.json()["pk"] == 1


# def test_aaa(ponydb, cli):
#     a = {"nom": "Mokmomokok", "prenom": "Ljlijjlj", "ddn": "1234-12-12", "sexe": "f"}
#     p = ponydb.Patient(**a)
#     assert p.to_dict()["pk"] == 1
#     r = cli.post("/patients/", data=json.dumps(a))
#     print(r.json())
