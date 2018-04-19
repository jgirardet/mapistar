# Standard Libraries
from datetime import date
from string import capwords

# Third Party Libraries
from apistar import Include, Route, http, types, validators
from mapistar.base_db import db
from pony.orm import Optional, PrimaryKey, Required, Set
from typing import List

# from mapistar.models import db
from .shortcuts import get_or_404


MAX_LENGTH = {
    "nom": 100,
    "prenom": 100,
    "sexe": 1,
    "rue": 200,
    "ville": 100,
    "tel": 20,
    "email": 100,
}

SEXE = ["f", "m"]

MAX = {"cp": 10000000}


class Patient(db.Entity):
    """
    Base class pour les patients

    Attributes:
        pk(int): clé primaire
    """

    pk = PrimaryKey(int, auto=True)
    nom = Required(str, MAX_LENGTH["nom"])
    prenom = Required(str, MAX_LENGTH["prenom"])
    ddn = Required(date)
    sexe = Required(str, MAX_LENGTH["sexe"], py_check=lambda x: x in SEXE)
    rue = Optional(str, MAX_LENGTH["rue"])
    cp = Optional(int, max=MAX["cp"])
    ville = Optional(str, MAX_LENGTH["ville"])
    tel = Optional(str, MAX_LENGTH["tel"])
    email = Optional(str, MAX_LENGTH["email"])
    alive = Optional(bool, default=True)
    actes = Set("Acte")

    def __repr__(self):
        """
        nice printing Firstname Name
        """
        return f"[Patient: {self.prenom} {self.nom}]"

    @property
    def dico(self):
        " return to_dict but serializable"
        _dico = self.to_dict()
        _dico["ddn"] = _dico["ddn"].isoformat()
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


class PatientCreateSchema(types.Type):
    nom = validators.String(max_length=MAX_LENGTH["nom"])
    prenom = validators.String(max_length=MAX_LENGTH["prenom"])
    ddn = validators.Date()
    sexe = validators.String(
        description="sexe", max_length=MAX_LENGTH["sexe"], enum=SEXE
    )


class PatientUpdateSchema(types.Type):
    nom = validators.String(max_length=MAX_LENGTH["nom"], default="")
    prenom = validators.String(max_length=MAX_LENGTH["prenom"], default="")
    ddn = validators.Date(default="")
    sexe = validators.String(enum=SEXE, default=None, allow_null=True)
    rue = validators.String(description="rue", max_length=MAX_LENGTH["rue"], default="")
    cp = validators.Integer(description="Code Postal", default=None, allow_null=True)
    ville = validators.String(
        description="Ville", max_length=MAX_LENGTH["ville"], default=""
    )
    tel = validators.String(
        description="Numéro de Téléphone", max_length=MAX_LENGTH["tel"], default=""
    )
    email = validators.String(
        description="email", max_length=MAX_LENGTH["email"], default=""
    )
    alive = validators.Boolean(description="vivant ?", default=True)


def add(patient: PatientCreateSchema) -> http.JSONResponse:
    """
    create patients
    """
    a = db.Patient(**patient)
    return http.JSONResponse(a.dico, status_code=201)


def liste() -> List[dict]:
    """ List patients """
    return [x.dico for x in db.Patient.select()]


def get(pk: int) -> dict:
    """ Get patient details """
    return get_or_404(db.Patient, pk).dico


def delete(pk: int) -> dict:
    """delete un patient"""
    pat = get_or_404(db.Patient, pk)
    pat.delete()
    return {"msg": "delete success"}


def update(new_data: PatientUpdateSchema, pk: int) -> http.JSONResponse:
    """ modify patients """
    to_update = get_or_404(db.Patient, pk)
    to_update.set(**{k: v for k, v in new_data.items() if v})
    return http.JSONResponse(to_update.dico, status_code=201)


routes_patients = Include(
    url="/patients",
    name="patients",
    routes=[
        Route(url="/", method="POST", handler=add),
        Route(url="/", method="GET", handler=liste),
        Route(url="/{pk}/", method="PUT", handler=update),
        Route(url="/{pk}/", method="DELETE", handler=delete),
        Route(url="/{pk}/", method="GET", handler=get),
    ],
)
#
