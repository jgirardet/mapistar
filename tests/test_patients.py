import pytest

from mapistar.patients.models import Patient

pytestmark = pytest.mark.pony
import datetime


def test_essai():
    Patient(nom="omkmo", prenom="omkmok", ddn="1234-12-12")
    Patient(nom="omkmo", prenom="omkmok", ddn="1234-12-12")
    Patient(nom="omkmo", prenom="omkmok", ddn="1234-12-12")
    Patient(nom="omkmo", prenom="omkmok", ddn="1234-12-12")
    a = Patient.select()
    print(list(a))
    assert len(a) == 4


@pytest.mark.pony(reset_db=False)
def test_db(ponydb):
    ponydb.Patient(nom="omkmo", prenom="omkmok", ddn="1234-12-12")
    ponydb.Patient(nom="omkmo", prenom="omkmok", ddn="1234-12-12")
    ponydb.Patient(nom="omkmo", prenom="omkmok", ddn="1234-12-12")
    ponydb.Patient(nom="omkmo", prenom="omkmok", ddn="1234-12-12")
    a = ponydb.Patient.select()
    assert len(a) == 8