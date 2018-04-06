# Standard Libraries
import random

# Third Party Libraries
# import faker
from mapistar.models import db

from mimesis import Generic

# f = faker.Faker('fr_FR')
f = Generic('fr')


def patientd():
    """ patient dict sans id """
    return {
        "nom": f.person.last_name(),
        "prenom": f.person.name(),
        "ddn": Generic().datetime.date(),
        # "sexe": random.choice(('f', 'm')),
        "sexe": f.person.gender()[0].lower()
    }


def patient():
    """ patient """
    return db.Patient(**patientd())


def userd():
    return {
        'username': f.person.username(),
        'password': 'j',
        'nom': f.person.last_name(),
        'prenom': f.person.name()
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
        kwargs['motif'] = f.text.sentence()

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
