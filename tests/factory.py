# Third Party Libraries
import faker
import pytest

import random

f = faker.Faker('fr_FR')

patient_dict = {
    "nom": f.name(),
    "prenom": f.first_name(),
    "ddn": f.date(),
    "sexe": random.choice(('f', 'm')),
}


@pytest.fixture(scope='function')
def patientd(patient):
    """ patient dict sans id """
    dico = patient.to_dict(exclude='pk')
    patient.delete()
    return dico


@pytest.fixture(scope='function')
def patient(ponydb):
    """ patient dict sans id """
    a = ponydb.Patient(**patient_dict)
    a.flush()
    print(a)
    return a
