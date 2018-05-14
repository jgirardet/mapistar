import pytest
import json
from pony import orm
from tests.factory import userf, observationf
from mapistar.app import app
from apistar.test import TestClient

# pytestmark = pytest.mark.pony(reset_db=False)


# Third Party Libraries
from mimesis import Generic


@pytest.fixture(scope="session")
def clij(request):
    cli = TestClient(app)
    r = cli.post(
        app.reverse_url("users:login"),
        data=json.dumps({"username": "j", "password": "j"}),
    )
    token = r.content.decode()
    cli.headers.update({"Authorization": f"Bearer {token}"})

    return cli


@pytest.fixture(scope="session")
def clik(request):
    cli = TestClient(app)
    r = cli.post(
        app.reverse_url("users:login"),
        data=json.dumps({"username": "k", "password": "j"}),
    )
    token = r.content.decode()
    cli.headers.update({"Authorization": f"Bearer {token}"})

    return cli


def test_authentication():
    cli = TestClient(app)
    r = cli.get(app.reverse_url("patients:liste"))
    assert r.status_code == 401

    r = cli.post(
        app.reverse_url("users:login"),
        data=json.dumps({"username": "jjj", "password": "j"}),
    )
    assert r.status_code == 403

    r = cli.post(
        app.reverse_url("users:login"),
        data=json.dumps({"username": "j", "password": "jjj"}),
    )
    assert r.status_code == 403

    r = cli.post(
        app.reverse_url("users:login"),
        data=json.dumps({"username": "j", "password": "j"}),
    )
    assert r.status_code == 200

    token = r.content.decode()
    cli.headers.update({"Authorization": f"Bearer FZEFZEFEFZEF"})

    r = cli.get(app.reverse_url("patients:liste"))
    assert r.status_code == 401

    cli.headers.update({"Authorization": f"Bearer {token}"})
    r = cli.get(app.reverse_url("patients:liste"))
    assert r.status_code == 200


def test_patients(clij, clik):
    a = {"nom": "aaa", "prenom": "paa", "ddn": "1234-12-12", "sexe": "f"}
    resp = clij.post(app.reverse_url("patients:add"), data=json.dumps(a))
    assert resp.json()["id"] is not None

    liste = clij.get(app.reverse_url("patients:liste")).json()
    assert len(liste) == 9
    pat = liste[4]
    assert pat["id"] == 5

    pat2 = clij.get(app.reverse_url("patients:one", patient_id=5)).json()
    assert pat2 == pat

    resp = clij.delete(app.reverse_url("patients:delete", patient_id=5)).json()
    assert resp == {"msg": "delete success"}

    liste = clij.get(app.reverse_url("patients:liste")).json()
    assert len(liste) == 8
    assert [1, 2, 3, 4, 6, 7, 8, 9] == [i["id"] for i in liste]

    patient2 = liste[1]
    assert patient2["id"] == 2
    update = {"prenom": "omkmok", "ddn": "1237-03-03", "rue": "mokmokmok"}
    r = clij.put(
        app.reverse_url("patients:update", patient_id=2), data=json.dumps(update)
    ).json()
    assert (
        r
        == {
            "id": 2,
            "nom": patient2["nom"],
            "prenom": "Omkmok",
            "ddn": "1237-03-03",
            "sexe": patient2["sexe"],
            "rue": "mokmokmok",
            "cp": None,
            "ville": "",
            "tel": "",
            "email": "",
            "alive": True,
        }
    )


def test_observation(clij, clik):
    r = clij.get(app.reverse_url("observations:liste", patient_id=1)).json()
    assert [1, 1, 1, 2, 2, 2] == [r["owner"] for r in r]

    a = {"patient": 1, "motif": "omk", "body": "mkmok"}
    r = clij.post(app.reverse_url("observations:add"), data=json.dumps(a))
    assert r.status_code == 201
    tmp = r.json()["id"]

    r = clik.delete(app.reverse_url("observations:delete", acte_id=tmp))
    assert r.status_code == 403

    r = clij.delete(app.reverse_url("observations:delete", acte_id=tmp))
    assert r.status_code == 200

    r = clik.get(app.reverse_url("observations:one", acte_id=tmp))
    assert r.status_code == 404

    upd = {"motif": "mokmokmok"}
    r = clik.put(
        app.reverse_url("observations:update", acte_id=3), data=json.dumps(upd)
    )

    assert r.status_code == 403
    r = clij.put(
        app.reverse_url("observations:update", acte_id=3), data=json.dumps(upd)
    )

    assert r.status_code == 200
    assert r.json()["motif"] == "mokmokmok"

    r = clij.get(app.reverse_url("observations:one", acte_id=3))
    assert r.status_code == 200
    assert r.json()["motif"] == "mokmokmok"


def test_ordonnance(clij, clik, ponydb):
    r = clij.get(app.reverse_url("ordonnances:liste", patient_id=1)).json()
    assert [1, 1, 1, 2, 2, 2] == [r["owner"] for r in r]

    a = {"patient": 1}
    r = clij.post(app.reverse_url("ordonnances:add"), data=json.dumps(a))
    assert r.status_code == 201

    r = clik.delete(app.reverse_url("ordonnances:delete", acte_id=13))
    assert r.status_code == 403

    r = clij.delete(app.reverse_url("ordonnances:delete", acte_id=13))
    assert r.status_code == 200

    r = clik.get(app.reverse_url("ordonnances:one", acte_id=13))
    assert r.status_code == 404

    upd = {"ordre": "12-45-20"}
    r = clik.put(
        app.reverse_url("ordonnances:update", acte_id=14), data=json.dumps(upd)
    )

    assert r.status_code == 403
    r = clij.put(
        app.reverse_url("ordonnances:update", acte_id=14), data=json.dumps(upd)
    )

    assert r.status_code == 200
    assert r.json()["ordre"] == "12-45-20"

    r = clij.get(app.reverse_url("ordonnances:one", acte_id=14))
    assert r.status_code == 200
    assert r.json()["ordre"] == "12-45-20"

    r = clij.get(app.reverse_url("ordonnances:one", acte_id=17)).json()
    assert r["ordre"] == "1-2-3"

    upd = {"ordre": "3-1-2"}
    r = clij.put(
        app.reverse_url("ordonnances:update", acte_id=17), data=json.dumps(upd)
    )
    assert r.status_code == 403

    r = clik.put(
        app.reverse_url("ordonnances:update", acte_id=17), data=json.dumps(upd)
    )
    assert r.status_code == 200
    assert [i["id"] for i in r.json()["items"]] == [3, 1, 2]

    new = {"ordonnance": 17, "cip": "1234567890123", "nom": "Un Médoc"}
    r = clik.post(app.reverse_url("medicaments:add_item"), data=json.dumps(new))
    assert r.status_code == 201
    assert r.json()["id"] == 4

    r = clij.delete(app.reverse_url("medicaments:delete_item", item_id=4))
    assert r.status_code == 403

    r = clik.delete(app.reverse_url("medicaments:delete_item", item_id=4))
    assert r.status_code == 200
    assert r.json() == {"id": 4, "deleted": True}

    upd = {"duree": 32}
    r = clij.put(
        app.reverse_url("medicaments:update_item", item_id=3), data=json.dumps(upd)
    )
    assert r.status_code == 403

    r = clik.put(
        app.reverse_url("medicaments:update_item", item_id=3), data=json.dumps(upd)
    )
    assert r.status_code == 200
    assert r.json()["duree"] == 32
