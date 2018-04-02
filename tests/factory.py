# Standard Libraries
import random

# Third Party Libraries
import faker
from mapistar.models import db

f = faker.Faker('fr_FR')


def patientd():
    """ patient dict sans id """
    return {
        "nom": f.name(),
        "prenom": f.first_name(),
        "ddn": f.date(),
        "sexe": random.choice(('f', 'm')),
    }


def patient():
    """ patient """
    return db.Patient(**patientd())


def userd():
    return {
        'username': f.profile()['username'],
        'password': 'j',
        'nom': f.name(),
        'prenom': f.first_name()
    }


def user():
    """ simple user """
    return db.User.create_user(**userd())


def acte(p=None, u=None):
    p = p if p else patient()
    u = u if u else user()
    return db.Acte(patient=p, owner=u)


def observation(**kwargs):
    """ simple user """
    if not 'patient' in kwargs:
        kwargs['patient'] = patient()
    if not 'owner' in kwargs:
        kwargs['owner'] = user()
    if not 'motif' in kwargs:
        kwargs['motif'] = f.sentence()

    return db.Observation(**kwargs)


from pony.orm import commit


def ordonnance(**kwargs):
    if not 'patient' in kwargs:
        kwargs['patient'] = patient()
    if not 'owner' in kwargs:
        kwargs['owner'] = user()
    # commit()
    return db.Ordonnance(**kwargs)


def medicament(**kwargs):
    if not 'ordonnance' in kwargs:
        kwargs['ordonnance'] = ordonnance()
    if not 'cip' in kwargs:
        kwargs['cip'] = f.ean(8)
    if not 'nom' in kwargs:
        kwargs['nom'] = f.bs()
    return db.Medicament(**kwargs)
