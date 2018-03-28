# Standard Libraries
import random

# Third Party Libraries
import faker
import pytest

from pony import orm

f = faker.Faker('fr_FR')

from mapistar.models import db

# pytestmark = pytest.mark.pony


@pytest.fixture(scope='session')
def fk(request):
    return f


# @pytest.fixture(scope='function')
def patientd():
    """ patient dict sans id """
    return {
        "nom": f.name(),
        "prenom": f.first_name(),
        "ddn": f.date(),
        "sexe": random.choice(('f', 'm')),
    }


@pytest.fixture(scope='function')
def patient():
    """ patient """
    with orm.db_session:
        a = db.Patient(**patientd())
        a.flush()
    return a


# @pytest.fixture(scope='function')
def userd():
    return {
        'username': f.profile()['username'],
        'password': 'j',
        'nom': f.name(),
        'prenom': f.first_name()
    }


@pytest.fixture(scope='function')
def user():
    """ simple user """
    with orm.db_session():
        a = db.User.create_user(**userd())
        a.flush()
    return a


@pytest.fixture(scope='function')
def acte(patient, user):
    """ simple user """
    with orm.db_session():
        b = db.Acte(patient=patient.pk, owner=user.pk)
        b.flush()
    return b


@pytest.fixture(scope='function')
def observation(patient, user, motif=f.sentence()):
    """ simple user """
    with orm.db_session():
        b = db.Observation(patient=patient.pk, owner=user.pk, motif=motif)
        b.flush()
    return b


@pytest.fixture(scope='function')
def ordonnance(patient, user):
    """ simple user """
    with orm.db_session():
        b = db.Ordonnance(patient=patient.pk, owner=user.pk)
        b.flush()
    return b


# @pytest.fixture(scope='function')
# def patient(ponydb):
#     """ patient dict s ans id """
#     a = ponydb.Patient(**patient_dict)
#     ponydb.commit()
#     return a

# @pytest.fixture(scope='function')
# def user(ponydb):
#     """ simple user """
#     a = ponydb.User.create_user(username = f.profile()['username'], password='j', nom=f.name(), prenom = f.first_name())
#     ponydb.commit()
#     return a

# @pytest.fixture(scope='function')
# def acte(ponydb, patient, user):
#     """ simple user """
#     b = ponydb.Acte(patient = patient, owner=user)
#     ponydb.commit()
#     return b
