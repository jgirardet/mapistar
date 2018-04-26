# Standard Libraries
import random

# Third Party Libraries
from mimesis import Generic

# mapistar
from mapistar.db import db

f = Generic("fr")


def patientd():
    """ patient dict sans id """
    return {
        "nom": f.person.last_name(),
        "prenom": f.person.name(),
        "ddn": Generic().datetime.date(),
        # "sexe": random.choice(('f', 'm')),
        "sexe": f.person.gender()[0].lower(),
    }


def patientf():
    """ patient """
    return db.Patient(**patientd())


def userd():
    return {
        "username": f.person.username(),
        "password": "j",
        "nom": f.person.last_name(),
        "prenom": f.person.name(),
    }


def userf(**kwargs):
    """ simple user """
    if "username" not in kwargs:
        kwargs["username"] = f.person.username()
    if "password" not in kwargs:
        kwargs["password"] = "j"
    if "nom" not in kwargs:
        kwargs["nom"] = f.person.last_name()
    if "prenom" not in kwargs:
        kwargs["prenom"] = f.person.name()
    return db.User.create_user(**kwargs)


def actef(p=None, u=None):
    p = p if p else patientf()
    u = u if u else userf()
    return db.Acte(patient=p, owner=u)


def observationf(**kwargs):
    """ simple user """
    if "patient" not in kwargs:
        kwargs["patient"] = patientf()
    if "owner" not in kwargs:
        kwargs["owner"] = userf()
    if "motif" not in kwargs:
        kwargs["motif"] = f.text.sentence()

    return db.Observation(**kwargs)


def ordonnancef(**kwargs):
    if "patient" not in kwargs:
        kwargs["patient"] = patientf()
    if "owner" not in kwargs:
        kwargs["owner"] = userf()
    return db.Ordonnance(**kwargs)


def itemf(**kwargs):
    if "ordonnance" not in kwargs:
        kwargs["ordonnance"] = ordonnancef()
    return db.Item(**kwargs)


def medicamentf(**kwargs):
    if "ordonnance" not in kwargs:
        kwargs["ordonnance"] = ordonnancef()
    if "cip" not in kwargs:
        kwargs["cip"] = f.code.ean()
    if "nom" not in kwargs:
        kwargs["nom"] = f.food.drink()
    return db.Medicament(**kwargs)
