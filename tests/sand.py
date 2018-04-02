import sys

sys.path.append("/home/jim/dev/maison/mapistar")
from mapistar.models import db

from pony.orm import db_session
import random


def fake_patient():
    return db.Patient(nom="fake", prenom="fake", ddn="1234-12-12", sexe="f")


def fake_user():
    u = db.User.create_user(
        **{
            'username': 'fakeuser' + str(random.random()),
            'password': 'j',
            'nom': "fake",
            'prenom': "fake"
        })
    return u


def fake_acte(patient=None, owner=None):
    # print("apres if", p.pk)
    p = patient if patient else fake_patient()
    u = owner if owner else fake_user()
    return db.Acte(patient=p, owner=u)


"""
>>> p = fake_patient() # it's ok
>>> a = fake_acte() # its ok
>>> p2 = fake_acte(patient = p) # Error : TransactionError: An attempt to mix objects belonging to different transactions
# """

# with db_session():
#     p = fake_patient()  # it's ok
#     print(p.to_dict())
#     # print(p.pk)
#     a = fake_acte()  # its ok
#     print(a.to_dict())
#     p2 = fake_acte(patient=p)
#     print(p2.to_dict())
#     p3 = fake_acte(patient=a.patient, owner=a.owner)
#     print(p3.to_dict())
