# Standard Libraries
from datetime import date
from string import capwords
from typing import List

# Third Party Libraries
from apistar import Link, Section, http, types, validators
from apistar.exceptions import BadRequest
from pony.orm import Optional, PrimaryKey, Required, db_session

# mapistar
from mapistar.base_db import db
# from mapistar.models import db
from .shortcuts import get_or_404

MAX_LENGTH = {
    "nom": 100,
    "prenom": 100,
    "sexe": 1,
    "rue": 200,
    "cp": 10000000,
    "ville": 100,
    "tel": 20,
    "email": 100,
}

SEXE = ['m', 'f']


class Patient(db.Entity):

    pk = PrimaryKey(int, auto=True)
    nom = Required(str, MAX_LENGTH['nom'])
    prenom = Required(str, MAX_LENGTH['prenom'])
    ddn = Required(date)
    sexe = Required(
        str, MAX_LENGTH['sexe'], py_check=lambda x: x in ['m', 'f'])
    rue = Optional(str, MAX_LENGTH['rue'])
    cp = Optional(int, max=MAX_LENGTH['cp'])
    ville = Optional(str, MAX_LENGTH['ville'])
    tel = Optional(str, MAX_LENGTH['tel'])
    email = Optional(str, MAX_LENGTH['email'])
    alive = Optional(bool, default=True)

    def __repr__(self):
        """
        nice printing Firstname Name
        """
        return f"[Patient: {self.prenom} {self.nom}]"

    def _capwords(self):

        self.nom = capwords(self.nom)
        self.prenom = capwords(self.prenom)

    def before_insert(self):
        self.alive = True
        self._capwords()

    def before_update(self):
        self._capwords()


"""
champs à ajouter :
date de décès
décédé
médecin traitant déclaré
notes divers
"""


class PatientSchema(types.Type):
    pk = validators.Integer(default=None, allow_null=True)
    nom = validators.String(default='')
    prenom = validators.String(default='')
    ddn = validators.Date(default='')
    sexe = validators.String(default='')
    rue = validators.String(description="rue", default='')
    cp = validators.Integer(
        description="Code Postal", default=None, allow_null=True)
    ville = validators.String(description="Ville", default='')
    tel = validators.String(description="Numéro de Téléphone", default='')
    email = validators.String(description="email", default="")
    alive = validators.Boolean(description="vivant ?", default=True)


class PatientCreateSchema(types.Type):
    nom = validators.String(max_length=MAX_LENGTH['nom'])
    prenom = validators.String(max_length=MAX_LENGTH['prenom'])
    ddn = validators.Date()
    sexe = validators.String(description="sexe", max_length=MAX_LENGTH['sexe'])


class PatientUpdateSchema(types.Type):
    nom = validators.String(max_length=MAX_LENGTH['nom'], default='')
    prenom = validators.String(max_length=MAX_LENGTH['prenom'], default='')
    ddn = validators.Date(default='')
    sexe = validators.String(
        description="sexe", max_length=MAX_LENGTH['sexe'], default='')
    rue = validators.String(
        description="rue", max_length=MAX_LENGTH['rue'], default='')
    cp = validators.Integer(
        description="Code Postal", default=None, allow_null=True)
    ville = validators.String(
        description="Ville", max_length=MAX_LENGTH['ville'], default='')
    tel = validators.String(
        description="Numéro de Téléphone",
        max_length=MAX_LENGTH['tel'],
        default='')
    email = validators.String(
        description="email", max_length=MAX_LENGTH['email'], default="")
    alive = validators.Boolean(description="vivant ?", default=True)


@db_session
def add(patient: PatientCreateSchema) -> http.Response:
    """
    create patients
    """
    a = db.Patient(**patient)
    return http.Response(a.to_dict(), status_code=201)


@db_session
def liste() -> List[PatientSchema]:
    """ List patients """
    return [x.to_dict() for x in db.Patient.select()]


@db_session
def get(pk: int) -> PatientSchema:
    """ Get patient details """
    print("helloooooooooooooooooo")

    return get_or_404(db.Patient, pk).to_dict()


@db_session
def delete(pk: int) -> dict:
    """delete un patient"""
    pat = get_or_404(db.Patient, pk)
    pat.delete()
    return {"msg": "delete success"}


def update(new_data: PatientUpdateSchema, pk: int) -> PatientSchema:
    """ modify patients """
    to_update = get_or_404(db.Patient, pk)
    to_update.set(**{k: v for k, v in new_data.items() if v})
    return http.Response(to_update.to_dict(), status_code=201)


section_patients = Section(
    name="patients",
    content=[
        Link(url="/patients/", method="POST", handler=add),
        Link(url="/patients/", method="GET", handler=liste),
        Link(url="/patients/{pk}/", method="PUT", handler=update),
        # Link(url="/patients/", method="DELETE", handler=delete),
        Link(url="/patients/{pk}/", method="DELETE", handler=delete),
        Link(url="/patients/{pk}/", method="GET", handler=get),
    ],
    title="titre de section patieny",
    description="descriptoin Api des patients")
