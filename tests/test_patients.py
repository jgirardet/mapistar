# Standard Libraries
import json
from string import capwords

# Third Party Libraries
import pytest
from apistar.document import Document, Link
from apistar.exceptions import NotFound
from pony import orm
from .factory import patient

# mapistar
from mapistar.patients import PatientSchema

pytestmark = pytest.mark.pony

# @pytest.mark.usefixtures('patientd')
attrs = ('name', 'firstname')


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
        d = {
            'nom': "ZEFZEF",
            'prenom': "SDFSDF",
            'ddn': "1234-12-12",
            'sexe': 'm'
        }
        a = ponydb.Patient(**d)
        a.flush()
        for i in ['nom', 'prenom']:
            d[i] = capwords(d[i])
        assert a.nom == d['nom']
        assert a.prenom == d['prenom']

    def test_fileds_with_capwords_at_update(self, patient, ponydb):
        patient.nom = "FZEFZEFZEFEZF"
        patient.prenom = "sdfsdfdfsdfsdf sdfsdfsdf"
        orm.commit()
        assert patient.nom == "Fzefzefzefezf"
        assert patient.prenom == "Sdfsdfdfsdfsdf Sdfsdfsdf"


class TestPatientViews:
    def test_cli_patient_create(self, cli, app, ponydb):
        a = {
            'nom': "Mokmomokok",
            'prenom': "Ljlijjlj",
            'ddn': "1234-12-12",
            "sexe": "m"
        }

        resp = cli.post(app.reverse_url('patients:add'), data=json.dumps(a))
        assert resp.json() == PatientSchema(ponydb.Patient[1].to_dict())

    def test_cli_get_patient(self, patient, cli, app):
        resp = cli.get(app.reverse_url('patients:get', pk=patient.pk))
        assert resp.json() == PatientSchema(patient.to_dict())

    def test_cli_del_patient(self, patient, cli, app):
        resp = cli.delete('/patients/1/')
        # app.reverse_url('patients:delete', pk=patient.pk))
        assert resp.json() == {"msg": "delete success"}

    def test_cli_list_patient(self, ponydb, cli, app):
        e = []
        for i in range(5):
            e.append(patient(ponydb))
        orm.commit()
        resp = cli.get(app.reverse_url('patients:liste'))
        assert set(i['nom'] for i in resp.json()) == set(i.nom for i in e)

    def test_patient_update(self, patient, cli, app):
        print(patient.to_dict())
        update = {
            "prenom": "omkmok",
            "ddn": "1237-03-03",
            "rue": "mokmokmok",
        }
        response = cli.put(
            app.reverse_url('patients:update', pk=patient.pk),
            data=json.dumps(update))
        # assert False
        assert response.json() == PatientSchema(patient.to_dict())
        assert response.status_code == 201

    # # test read write
    # def test_patient_correpted_data(ss):
    #     "should not fail with corrupted date, because of readonly schema"
    #     a = Patient(name="ùlùlù#", firstname="mkljlij", birthdate="1234-12-12")
    #     a.save()
    #     patients_detail(ss, a.id)
    #     patients_list(ss)