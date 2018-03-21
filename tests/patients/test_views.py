# Standard Libraries
import json

# Third Party Libraries
import pytest
from apistar.exceptions import NotFound
from mapistar.patients import PatientSchema

from apistar.document import Document, Link
from pony import orm

from tests.factory import patient

pytestmark = pytest.mark.pony


def test_cli_patient_create(cli, app, ponydb):
    a = {'nom': "Mokmomokok", 'prenom': "Ljlijjlj", 'ddn': "1234-12-12"}

    resp = cli.post(app.reverse_url('patients:add'), data=json.dumps(a))
    assert resp.json() == PatientSchema(ponydb.Patient[1].to_dict())


def test_cli_get_patient(patient, cli, app):
    resp = cli.get(app.reverse_url('patients:get', pk=patient.pk))
    assert resp.json() == PatientSchema(patient.to_dict())


def test_cli_del_patient(patient, cli, app):
    resp = cli.delete('/patients/1/')
    # app.reverse_url('patients:delete', pk=patient.pk))
    assert resp.json() == {"msg": "delete success"}


def test_cli_list_patient(ponydb, cli, app):
    e = []
    for i in range(5):
        e.append(patient(ponydb))
    orm.commit()
    resp = cli.get(app.reverse_url('patients:liste'))
    assert set(i['nom'] for i in resp.json()) == set(i.nom for i in e)


# # test read write
# def test_patient_correpted_data(ss):
#     "should not fail with corrupted date, because of readonly schema"
#     a = Patient(name="ùlùlù#", firstname="mkljlij", birthdate="1234-12-12")
#     a.save()
#     patients_detail(ss, a.id)
#     patients_list(ss)


def test_patient_update(patient, cli, app):

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
