# Standard Libraries
import json
from datetime import timedelta

# Third Party Libraries
import pytest
from apistar.test import TestClient
from pony import orm

# mapistar
from mapistar.app import app

from .runner import generate_db


@pytest.fixture(scope="module")
def gen_db(ponydb):
    ponydb.drop_all_tables(with_all_data=True)
    ponydb.create_tables()
    generate_db()
    yield

    ponydb.drop_all_tables(with_all_data=True)
    ponydb.create_tables()  # do not interfer with pytest-ponyorm


pytestmark = pytest.mark.usefixtures("gen_db")


def test_authentication():
    # test need auth
    cli = TestClient(app)
    r = cli.get(app.reverse_url("patients:liste"))
    assert r.status_code == 401

    # test bad login
    r = cli.post(
        app.reverse_url("users:login"),
        data=json.dumps({"username": "jjj", "password": "j"}),
    )
    assert r.status_code == 403

    # test bad password
    r = cli.post(
        app.reverse_url("users:login"),
        data=json.dumps({"username": "j", "password": "jjj"}),
    )
    assert r.status_code == 403

    # test good login
    r = cli.post(
        app.reverse_url("users:login"),
        data=json.dumps({"username": "j", "password": "j"}),
    )
    assert r.status_code == 200

    token = r.content.decode()
    cli.headers.update({"Authorization": f"Bearer FZEFZEFEFZEF"})

    # test auth ok with header
    cli.headers.update({"Authorization": f"Bearer {token}"})
    r = cli.get(app.reverse_url("patients:liste"))
    assert r.status_code == 200


def test_patients(clij, clik):
    # test add
    a = {"nom": "aaa", "prenom": "paa", "ddn": "1234-12-12", "sexe": "f"}
    resp = clij.post(app.reverse_url("patients:add"), data=json.dumps(a))
    assert resp.json()["id"] is not None

    # test liste
    liste = clij.get(app.reverse_url("patients:liste")).json()
    assert len(liste) == 9
    pat = liste[4]
    assert pat["id"] == 5

    # test one
    pat2 = clij.get(app.reverse_url("patients:one", patient_id=5)).json()
    assert pat2 == pat

    # test delete fail bad Permission
    resp = clik.delete(app.reverse_url("patients:delete", patient_id=5)).json()
    assert resp == "Action non autorisée pour l'utilisateur k"

    # test delete fail bad Permission

    resp = clij.delete(app.reverse_url("patients:delete", patient_id=5)).json()
    assert resp == {"msg": "delete success"}

    liste = clij.get(app.reverse_url("patients:liste")).json()
    assert len(liste) == 8
    assert [1, 2, 3, 4, 6, 7, 8, 9] == [i["id"] for i in liste]

    # test update
    patient2 = liste[1]
    assert patient2["id"] == 2
    update = {"prenom": "omkmok", "ddn": "1237-03-03", "rue": "mokmokmok"}
    r = clij.put(
        app.reverse_url("patients:update", patient_id=2), data=json.dumps(update)
    ).json()
    assert r == {
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


def test_observation(clij, clik):
    # test liste
    r = clij.get(app.reverse_url("observations:liste", patient_id=1)).json()
    assert [1, 1, 1, 2, 2, 2] == [r["owner"] for r in r]

    # test add
    a = {"patient": 1, "motif": "omk", "body": "mkmok"}
    r = clij.post(app.reverse_url("observations:add"), data=json.dumps(a))
    assert r.status_code == 201
    tmp = r.json()["id"]

    # test delete bad owner
    r = clik.delete(app.reverse_url("observations:delete", acte_id=tmp))
    assert r.status_code == 403

    # test delete good owner
    r = clij.delete(app.reverse_url("observations:delete", acte_id=tmp))
    assert r.status_code == 200

    # test 404
    r = clik.get(app.reverse_url("observations:one", acte_id=tmp))
    assert r.status_code == 404

    # test udpate bad owner
    upd = {"motif": "mokmokmok"}
    r = clik.put(
        app.reverse_url("observations:update", acte_id=3), data=json.dumps(upd)
    )
    assert r.status_code == 403

    # test_update food owner
    r = clij.put(
        app.reverse_url("observations:update", acte_id=3), data=json.dumps(upd)
    )
    assert r.status_code == 200
    assert r.json()["motif"] == "mokmokmok"

    # test one
    r = clij.get(app.reverse_url("observations:one", acte_id=3))
    assert r.status_code == 200
    assert r.json()["motif"] == "mokmokmok"


def test_ordonnance(clij, clik):
    # test list
    r = clij.get(app.reverse_url("ordonnances:liste", patient_id=1)).json()
    assert [1, 1, 1, 2, 2, 2] == [r["owner"] for r in r]

    # test add
    a = {"patient": 1}
    r = clij.post(app.reverse_url("ordonnances:add"), data=json.dumps(a))
    assert r.status_code == 201

    # test delete bad owner
    r = clik.delete(app.reverse_url("ordonnances:delete", acte_id=13))
    assert r.status_code == 403

    # test delete good owner
    r = clij.delete(app.reverse_url("ordonnances:delete", acte_id=13))
    assert r.status_code == 200

    # test 404
    r = clik.get(app.reverse_url("ordonnances:one", acte_id=13))

    # test delete 404
    r = clik.delete(app.reverse_url("ordonnances:delete", acte_id=13))
    assert r.status_code == 404

    # test update bad owner
    upd = {"ordre": "12-45-20"}
    r = clik.put(
        app.reverse_url("ordonnances:update", acte_id=14), data=json.dumps(upd)
    )
    assert r.status_code == 403

    # test update ood owner
    r = clij.put(
        app.reverse_url("ordonnances:update", acte_id=14), data=json.dumps(upd)
    )
    assert r.status_code == 200
    assert r.json()["ordre"] == "12-45-20"

    # test  one
    r = clij.get(app.reverse_url("ordonnances:one", acte_id=14))
    assert r.status_code == 200
    assert r.json()["ordre"] == "12-45-20"

    # test item ordre
    r = clij.get(app.reverse_url("ordonnances:one", acte_id=17)).json()
    assert r["ordre"] == "1-2-3"

    # test item ordre
    upd = {"ordre": "3-1-2"}
    r = clik.put(
        app.reverse_url("ordonnances:update", acte_id=17), data=json.dumps(upd)
    )
    assert r.status_code == 200
    assert [i["id"] for i in r.json()["items"]] == [3, 1, 2]

    # test new item obj not ordo
    new = {"cip": "1234567890123", "nom": "Un Médoc"}
    r = clij.post(
        app.reverse_url("medicaments:add_item", acte_id=1), data=json.dumps(new)
    )
    assert r.status_code == 400
    assert r.json() == "acte_id doit correspondre à une ordonnance"

    # test new item
    r = clik.post(
        app.reverse_url("medicaments:add_item", acte_id=17), data=json.dumps(new)
    )
    assert r.status_code == 201
    assert r.json()["ordonnance"] == 17

    # test delete item bad user
    tmp = r.json()["id"]
    r = clij.delete(app.reverse_url("medicaments:delete_item", item_id=tmp))
    assert r.status_code == 403

    # test delete item good user
    r = clik.delete(app.reverse_url("medicaments:delete_item", item_id=tmp))
    assert r.status_code == 200
    assert r.json() == {"id": tmp, "deleted": True}

    # test item update bad owner
    upd = {"duree": 32}
    r = clij.put(
        app.reverse_url("medicaments:update_item", item_id=3), data=json.dumps(upd)
    )
    assert r.status_code == 403

    # test item update good owner
    r = clik.put(
        app.reverse_url("medicaments:update_item", item_id=3), data=json.dumps(upd)
    )
    assert r.status_code == 201
    assert r.json()["duree"] == 32

    # test item delete  first
    r = clik.delete(app.reverse_url("medicaments:delete_item", item_id=4))
    assert r.status_code == 200
    assert r.json() == {"id": 4, "deleted": True}

    # test item delete last
    r = clik.delete(app.reverse_url("medicaments:delete_item", item_id=6))
    assert r.status_code == 200
    assert r.json() == {"id": 6, "deleted": True}

    # test item delete one( only one item left)
    r = clik.delete(app.reverse_url("medicaments:delete_item", item_id=5))
    assert r.status_code == 200
    assert r.json() == {"id": 5, "deleted": True}

    # test bad order for items fallback
    upd = {"ordre": "3-1-2"}
    r = clij.put(
        app.reverse_url("ordonnances:update", acte_id=19), data=json.dumps(upd)
    )
    assert r.status_code == 200
    r = clij.get(app.reverse_url("ordonnances:one", acte_id=19))
    assert r.status_code == 200
    assert [x["id"] for x in r.json()["items"]] == [7, 8, 9]

    ################
    # test preciptions Libres
    ##################

    # test new divers
    r = clij.post(
        app.reverse_url("divers:add_item", acte_id=20),
        data=json.dumps({"texte": "aaaa"}),
    )
    assert r.status_code == 201
    assert r.json()["ordonnance"] == 20
    new_divers = r.json()["id"]

    # test update divers
    r = clij.put(
        app.reverse_url("divers:update_item", item_id=new_divers),
        data=json.dumps({"texte": "zerzer"}),
    )
    assert r.status_code == 201

    # assert r.json()["ordonnance"] ==


def test_permissions(clij, clik, ponydb):

    # test bad day
    with orm.db_session():
        a = ponydb.Acte[16]
        a.created = a.created - timedelta(days=1)
    r = clik.delete(app.reverse_url("ordonnances:delete", acte_id=16))
    assert r.json() == "Un acte ne peut être modifié en dehors du jours même"


def test_users(clij):
    # change password
    datak = {"old": "j", "new1": "new", "new2": "new"}
    r = clij.post(app.reverse_url("users:change_password"), data=json.dumps(datak))
    assert r.json()["msg"] == "password changed"

    # get get_new_password
    r = clij.get(app.reverse_url("users:get_new_password"))
    assert r.json().get("password", None)
