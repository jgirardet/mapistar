# Standard Libraries
import json
from datetime import timedelta

# Third Party Libraries
import pytest
from pony import orm

# mapistar
# from mapistar.documents import Document

from .runner import generate_db
from simple_settings import settings

from unittest.mock import patch

# from mapistar import main


@pytest.fixture(scope="module")
def gen_db(ponydb):
    ponydb.drop_all_tables(with_all_data=True)
    ponydb.create_tables()
    generate_db()
    yield

    ponydb.drop_all_tables(with_all_data=True)
    ponydb.create_tables()  # do not interfer with pytest-ponyorm


pytestmark = pytest.mark.usefixtures("gen_db")


def test_patients(clij, clik):
    # test add
    a = {"nom": "aaa", "prenom": "paa", "ddn": "1234-12-12", "sexe": "f"}
    r = clij.post("patients", {"data": a})
    assert "201" in r.status
    assert r.data == {
        "id": 9,
        "nom": "Aaa",
        "prenom": "Paa",
        "ddn": "1234-12-12",
        "sexe": "f",
        "rue": "",
        "cp": None,
        "ville": "",
        "tel": "",
        "email": "",
        "alive": True,
    }

    # test_get
    r = clij.get("/patients")
    assert "200" in r.status
    assert len(r.data) == 9
    assert "rue" in r.data[0].keys()

    r = clij.get("patients", {"patientid": 9})
    assert "200" in r.status
    assert r.data == {
        "id": 9,
        "nom": "Aaa",
        "prenom": "Paa",
        "ddn": "1234-12-12",
        "sexe": "f",
        "rue": "",
        "cp": None,
        "ville": "",
        "tel": "",
        "email": "",
        "alive": True,
    }

    # test update
    update = {"prenom": "omkmok", "ddn": "1237-03-03", "rue": "mokmokmok"}
    r = clij.put("/patients", {"patientid": 9, "data": update})
    assert r.data == {
        "id": 9,
        "nom": "Aaa",
        "prenom": "Omkmok",
        "ddn": "1237-03-03",
        "sexe": "f",
        "rue": "mokmokmok",
        "cp": None,
        "ville": "",
        "tel": "",
        "email": "",
        "alive": True,
    }

    # delete unauthorized
    r = clik.delete("/patients", {"patientid": 9})
    assert r.data == {"errors": {"Action non autorisée pour l'utilisateur k": None}}
    # test delete
    r = clij.delete("/patients", {"patientid": 9})
    assert r.data == {"msg": "delete success", "patientid": 9}


def test_users(cli_anonymous):
    cli = cli_anonymous

    # test need auth
    r = cli.get("/patients")
    assert "401" in r.status

    # test bad login
    r = cli.post("/users/login", {"username": "jjj", "password": "j"})
    assert "403" in r.status
    assert r.data == {"errors": {"Incorrect username or password.": None}}

    # test bad password
    r = cli.post("/users/login", username="j", password="jjj")
    assert "403" in r.status
    assert r.data == {"errors": {"Incorrect username or password.": None}}

    # test good login
    r = cli.post("/users/login", username="j", password="j")
    assert "200" in r.status
