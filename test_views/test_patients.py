# Standard Libraries
import json

# Third Party Libraries
import pytest
from pony import orm

pytestmark = pytest.mark.pony

# @pytest.mark.usefixtures('patientd')
attrs = ("name", "firstname")


def test_cli_patient_create(cli, app):
    a = {"nom": "Mokmomokok", "prenom": "Ljlijjlj", "ddn": "1234-12-12", "sexe": "m"}

    resp = cli.post(app.reverse_url("patients:add"), data=json.dumps(a))
    resp.json()["id"]
    assert resp.json()["id"] is not None


def test_cli_get_patient(patient, cli, app):
    resp = cli.get(app.reverse_url("patients:get", id=patient.id))
    assert resp.json() == patient.dico


def test_cli_del_patient(patient, cli, app):
    resp = cli.delete(app.reverse_url("patients:delete", id=patient.id))
    assert resp.json() == {"msg": "delete success"}


def test_cli_list_patient(patient, cli, app):
    e = []
    for i in range(5):
        e.append(patient)
    orm.commit()
    resp = cli.get(app.reverse_url("patients:liste"))
    assert {i["nom"] for i in resp.json()} == {i.nom for i in e}


def test_patient_update(patient, cli, app):
    patient.sexe = "m"
    patient.flush()
    update = {"prenom": "omkmok", "ddn": "1237-03-03", "rue": "mokmokmok"}
    response = cli.put(
        app.reverse_url("patients:update", id=patient.id), data=json.dumps(update)
    )
    for i in update:
        assert response.json() == patient.dico
    assert response.status_code == 201
