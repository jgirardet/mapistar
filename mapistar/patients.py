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


class Patient(db.Entity):

    pk = PrimaryKey(int, auto=True)
    nom = Required(str, MAX_LENGTH['nom'])
    prenom = Required(str, MAX_LENGTH['prenom'])
    ddn = Required(date)
    sexe = Required(
        str, MAX_LENGTH['sexe'], py_check=lambda x: x in [None, 'm', 'f'])
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
    pk = validators.Integer(default=None)
    nom = validators.String(max_length=MAX_LENGTH['nom'])
    prenom = validators.String(max_length=MAX_LENGTH['prenom'])
    ddn = validators.Date()
    sexe = validators.String(description="sexe", max_length=MAX_LENGTH['sexe'])
    rue = validators.String(
        description="rue", max_length=MAX_LENGTH['rue'], default="")
    cp: validators.Integer(description="Code Postal")
    ville: validators.String(
        description="Ville", max_length=MAX_LENGTH['ville'])
    # tel: validators.String(description="Numéro de Téléphone", max_length=MAX_LENGTH['tel'])
    # email: validators.String(description="email", max_length=MAX_LENGTH['email'])
    # alive: validators.Boolean(description="vivant ?")


class PatientUpdateSchema(PatientSchema):
    pk = validators.Integer(default=None)
    nom = validators.String(max_length=100, default=None)
    prenom = validators.String(max_length=100, default=None)
    ddn = validators.Date(default=None)
    # sexe = validators.Boolean(description="sexe", default=False)
    rue = validators.String(description="rue", default=None)


@db_session
def add(patient: PatientSchema) -> http.Response:
    """
    create patients
    """
    if 'pk' is not None in patient:
        raise BadRequest("pk ne peut être spédicifée pour un ajout")
    # print(patient)
    a = db.Patient(**patient)
    return http.Response(PatientSchema(a.to_dict()), status_code=201)


@db_session
def liste() -> List[PatientSchema]:
    """ List patients """
    return [PatientSchema(x.to_dict()) for x in db.Patient.select()]


@db_session
def get(pk: int) -> PatientSchema:
    """ Get patient details """
    print("helloooooooooooooooooo")

    pat = get_or_404(db.Patient, pk)
    return PatientSchema(pat)


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
    return http.Response(PatientSchema(to_update.to_dict()), status_code=201)


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
