# Standard Libraries
import json
from datetime import timedelta

# Third Party Libraries
import pytest
from pony import orm

# mapistar
# from mapistar.documents import Document

from runner import generate_db
from simple_settings import settings

from unittest.mock import patch
from mapistar import main


@pytest.fixture(scope="module")
def gen_db(ponydb):
    ponydb.drop_all_tables(with_all_data=True)
    ponydb.create_tables()
    generate_db()
    yield

    ponydb.drop_all_tables(with_all_data=True)
    ponydb.create_tables()  # do not interfer with pytest-ponyorm


pytestmark = pytest.mark.usefixtures("gen_db")


# @pytest.mark.pony(reset_db=False)
def test_patients(clij):
    # test add
    a = {"nom": "aaa", "prenom": "paa", "ddn": "1234-12-12", "sexe": "f"}
    r = clij.post(main, "patients", {"data": a})
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
    r = clij.get(main, "patients")
    assert "200" in r.status
    assert len(r.data) == 9
    assert "rue" in r.data[0].keys()

    r = clij.get(main, "patients", {"patientid": 9})
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
    r = clij.put(main, "/patients", {"patientid": 9, "data": update})
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