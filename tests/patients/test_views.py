# Standard Libraries
import json

# Third Party Libraries
import pytest
from apistar.exceptions import NotFound
from mapistar.patients.views import patients_create
from mapistar.patients.schemas import PatientSchema

from apistar import http, test
from apistar.document import Document, Link
from apistar.server.app import App
from app import app


def test_patient_create():
    a = {'nom': "Mokmomokok", 'prenom': "Ljlijjlj", 'ddn': "1234-12-12"}

    resp = patients_create(PatientSchema(**a))
    assert resp.content == a


client = test.TestClient(app)


def test_cli_patient_create():
    a = {'nom': "Mokmomokok", 'prenom': "Ljlijjlj", 'ddn': "1234-12-12"}

    resp = client.post(app.reverse_url('add patient'), data=json.dumps(a))
    assert resp.json() == a
    # resp = json.loads(response.content.decode())

    # assert response.status_code == 201
    # assert Patient.objects.get(id=resp['id']).name.lower() == a['name'].lower()


# # test read write
# def test_patient_correpted_data(ss):
#     "should not fail with corrupted date, because of readonly schema"
#     a = Patient(name="ùlùlù#", firstname="mkljlij", birthdate="1234-12-12")
#     a.save()
#     patients_detail(ss, a.id)
#     patients_list(ss)

# # patients_detail
# def test_patient_detail(client, patient):
#     """
#     Testing a view, using the test client with
#     """
#     response = client.get(
#         reverse_url('patients_detail', patient_id=patient.id))
#     resp = json.loads(response.content.decode())
#     assert resp == PatientSchema(patient)

# def test_detail_not_found(ss, patient):
#     deleted = patient.id
#     patient.delete()
#     with pytest.raises(NotFound):
#         patients_detail(ss, deleted)

# def test_patient_list(client, patient10):
#     response = client.get(reverse_url('patients_list'))
#     resp = json.loads(response.content.decode())
#     assert resp == [PatientSchema(p) for p in Patient.objects.all()]

# def test_patient_update(patient, client):
#     response = client.put(
#         reverse_url('patients_update', patient_id=patient.id),
#         {"city": "Nevers"})
#     a = Patient.objects.get(id=patient.id)
#     assert a.city == "Nevers"

# def test_patient_update_raises_not_found(patient, ss):
#     a = patient.id
#     patient.delete()
#     with pytest.raises(NotFound):
#         patients_update(ss, a, PatientSchema())
