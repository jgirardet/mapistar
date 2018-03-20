# Standard Libraries
from string import capwords

# Third Party Libraries
import pytest

from pony import orm

pytestmark = pytest.mark.pony

# @pytest.mark.usefixtures('patientd')
"""
Class to Test Patient model
"""

attrs = ('name', 'firstname')


def test_string(ponydb):
    """
    test autoput of str
    """
    a = ponydb.Patient(nom="mok", prenom="omk", ddn="1234-12-12")

    assert a.__repr__() == "[Patient: omk mok]"


def test_fields_with_capwords_at_create(ponydb):
    """
    must be caps words :
        name
        firstname
    """
    d = {'nom': "ZEFZEF", 'prenom': "SDFSDF", 'ddn': "1234-12-12"}
    a = ponydb.Patient(**d)
    a.flush()
    for i in ['nom', 'prenom']:
        d[i] = capwords(d[i])
    assert a.nom == d['nom']
    assert a.prenom == d['prenom']


def test_fileds_with_capwords_at_update(patient, ponydb):
    patient.nom = "FZEFZEFZEFEZF"
    patient.prenom = "sdfsdfdfsdfsdf sdfsdfsdf"
    print(patient.nom, patient.id)
    orm.commit()
    print(patient.nom)
    print(ponydb.Patient.select()[:])
    assert patient.nom == "Fzefzefzefezf"
    assert patient.prenom == "Sdfsdfdfsdfsdf Sdfsdfsdf"


# def test_blank_true_for_non_required_fields(patientd):
#     """
#     mixer don't autopopulate blank fields
#     """
#     d = {i: patientd[i] for i in ['name', 'firstname', 'birthdate']}
#     a = Patient(
#         name=d['name'], firstname=d['firstname'], birthdate=d['birthdate'])
#     a.save()
#     b = Patient.objects.get(id=a.id)

#     assert a == b
