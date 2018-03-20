# Standard Libraries
import json

# Third Party Libraries
import pytest
from apistar.exceptions import NotFound
from mapistar.patients.schemas import PatientSchema

from apistar.document import Document, Link
from pony import orm

from tests.factory import patient

pytestmark = pytest.mark.pony


def test_cli_patient_create(cli, app):
    a = {'nom': "Mokmomokok", 'prenom': "Ljlijjlj", 'ddn': "1234-12-12"}

    resp = cli.post(app.reverse_url('patients:add'), data=json.dumps(a))
    a['pk'] = 1
    assert resp.json() == a


def test_cli_get_patient(patient, cli, app):
    resp = cli.get(app.reverse_url('patients:get', patient_pk=patient.pk))
    assert resp.json() == PatientSchema(patient.to_dict())


def test_cli_del_patient(patient, cli, app):
    resp = cli.delete(
        app.reverse_url('patients:delete', patient_pk=patient.pk))
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

    update = {"pk": patient.pk, "rue": "mokmokmok", "nom": "lùplùplù ùpl ù "}
    response = cli.put(app.reverse_url('patients:update', new_data=update))
    assert response.json() == PatientSchema(patient.to_dict())
