import pytest

import faker

f = faker.Faker()


@pytest.fixture(scope='function')
def patientd(ponydb):
    """ patient dict sans id """
    return (ponydb.Patient(nom=f.name(), prenom=f.first_name(), ddn=f.date())
            .to_dict(exclude='pk'))


@pytest.fixture(scope='function')
def patient(ponydb):
    """ patient dict sans id """
    a = ponydb.Patient(nom=f.name(), prenom=f.first_name(), ddn=f.date())
    a.flush()
    print(a)
    return a