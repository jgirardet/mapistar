# Standard Libraries
from pendulum import date
from string import capwords
from typing import List

# Third Party Libraries
from apistar import Include, Link, Route, Section, http, types, validators
from apistar.exceptions import BadRequest
from pony.orm import Optional, PrimaryKey, Required, db_session, Set

# mapistar
from mapistar.base_db import db

# from mapistar.models import db
from .shortcuts import get_or_404

import cerberus

from .utils import date_validator, MapistarValidator

patient_schema = {
    "nom": {
        "type": "string",
        "maxlength": 100,
        "required": True
    },
    "prenom": {
        "type": "string",
        "maxlength": 100,
        "required": True
    },
    "ddn": {
        "type": "string",
        "required": True,
        "validator": date_validator,
    },
    "sexe": {
        "type": "string",
        "maxlength": 1,
        "required": True,
        "allowed": ['m', 'f']
    },
    "rue": {
        "type": "string",
        "maxlength": 200
    },
    "cp": {
        "type": "integer",
        "max": 10000000,
    },
    "ville": {
        "type": "string",
        "maxlength": 100
    },
    "tel": {
        "type": "string",
        "maxlength": 20
    },
    "email": {
        "type": "string",
        "maxlength": 100
    },
    "alive": {
        "type": "boolean"
    },
}

PatientCreateSchema = MapistarValidator(patient_schema)

PatientUpdateSchema = MapistarValidator(patient_schema, update=True)


class Patient(db.Entity):

    pk = PrimaryKey(int, auto=True)
    nom = Required(str, patient_schema['nom']['maxlength'])
    prenom = Required(str, patient_schema['prenom']['maxlength'])
    ddn = Required(date)
    sexe = Required(
        str, py_check=lambda x: x in patient_schema['sexe']['allowed'])
    rue = Optional(str, patient_schema['rue']['maxlength'])
    cp = Optional(int, max=patient_schema['cp']['max'])
    ville = Optional(str, patient_schema['ville']['maxlength'])
    tel = Optional(str, patient_schema['tel']['maxlength'])
    email = Optional(str, patient_schema['email']['maxlength'])
    alive = Optional(bool, default=True)
    actes = Set('Acte')

    def __repr__(self):
        """
        nice printing Firstname Name
        """
        return f"[Patient: {self.prenom} {self.nom}]"

    @property
    def dico(self):
        " return to_dict but serializable"
        _dico = self.to_dict()
        _dico['ddn'] = _dico['ddn'].isoformat()
        return _dico

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

# class PatientCreateSchema(types.Type):
#     nom = validators.String(max_length=MAX_LENGTH['nom'])
#     prenom = validators.String(max_length=MAX_LENGTH['prenom'])
#     ddn = validators.Date()
#     sexe = validators.String(
#         description="sexe", max_length=MAX_LENGTH['sexe'], enum=SEXE)

# class PatientUpdateSchema(types.Type):
#     nom = validators.String(max_length=MAX_LENGTH['nom'], default='')
#     prenom = validators.String(max_length=MAX_LENGTH['prenom'], default='')
#     ddn = validators.Date(default='')
#     sexe = validators.String(enum=SEXE, default=None, allow_null=True)
#     rue = validators.String(
#         description="rue", max_length=MAX_LENGTH['rue'], default='')
#     cp = validators.Integer(
#         description="Code Postal", default=None, allow_null=True)
#     ville = validators.String(
#         description="Ville", max_length=MAX_LENGTH['ville'], default='')
#     tel = validators.String(
#         description="Numéro de Téléphone",
#         max_length=MAX_LENGTH['tel'],
#         default='')
#     email = validators.String(
#         description="email", max_length=MAX_LENGTH['email'], default="")
#     alive = validators.Boolean(description="vivant ?", default=True)


@db_session
def add(patient: PatientCreateSchema) -> http.Response:
    """
    create patients
    """
    a = db.Patient(**patient)
    return http.JSONResponse(a.dico, status_code=201)


@db_session
def liste() -> List[dict]:
    """ List patients """
    return [x.dico for x in db.Patient.select()]


@db_session
def get(pk: int) -> dict:
    """ Get patient details """
    return get_or_404(db.Patient, pk).dico


@db_session
def delete(pk: int) -> dict:
    """delete un patient"""
    pat = get_or_404(db.Patient, pk)
    pat.delete()
    return {"msg": "delete success"}


@db_session
def update(new_data: PatientUpdateSchema, pk: int) -> dict:
    """ modify patients """
    to_update = get_or_404(db.Patient, pk)
    to_update.set(**{k: v for k, v in new_data.items() if v})
    return http.JSONResponse(to_update.dico, status_code=201)


routes_patients = Include(
    url='/patients',
    name='patients',
    routes=[
        Route(url="/", method="POST", handler=add),
        Route(url="/", method="GET", handler=liste),
        Route(url="/{pk}/", method="PUT", handler=update),
        # Route(url="/patients/", method="DELETE", handler=delete),
        Route(url="/{pk}/", method="DELETE", handler=delete),
        Route(url="/{pk}/", method="GET", handler=get),
    ])
#
