# Standard Libraries
from datetime import date
from typing import List

# Third Party Libraries
# from apistar import Include, Route, exceptions, http, types, validators
from pony.orm import Optional, Required, Set, db_session

# mapistar
from mapistar.base_db import db

# from mapistar.users import User

# from mapistar.db import db
from mapistar.utils import get_or_404, CapWordsMixin

MAX_LENGTH = {
    "nom": 100,
    "prenom": 100,
    "sexe": 1,
    "rue": 200,
    "ville": 100,
    "tel": 20,
    "email": 100,
}


""" Valeurs maximales pour chaque field"""

SEXE = ["f", "m"]


class Patient(CapWordsMixin, db.Entity):
    """
    Entity Patient

    Attributes:
        nom (str): Nom du patient. Requis
        prenom (str): prenom du patient. Requis
        ddn (datetime.Datetime): date de naissance. Requis
        sexe (str): "m" ou "f". Requis
        rue (str): Rue
        cp(int): Code Postal
        ville(str): Ville
        tel(str): Téléphone
        email(str): E-mail
        alive(bool): Patient Vivant ou non.
        actes(mapistar.actes.models.Acte): Actes ratachés au patient.

    """

    nom = Required(str, MAX_LENGTH["nom"])
    prenom = Required(str, MAX_LENGTH["prenom"])
    ddn = Required(date)
    sexe = Required(str, MAX_LENGTH["sexe"], py_check=lambda x: x in SEXE)
    rue = Optional(str, MAX_LENGTH["rue"])
    cp = Optional(int)
    ville = Optional(str, MAX_LENGTH["ville"])
    tel = Optional(str, MAX_LENGTH["tel"])
    email = Optional(str, MAX_LENGTH["email"])
    alive = Optional(bool, default=True)
    # actes = Set("Acte")

    def __repr__(self):
        """
        nice printing Firstname Name
        """
        return f"[Patient: {self.prenom} {self.nom}]"

    def before_insert(self):
        """
        * La patient est spécifié vivant.
        * Nom et Prenom sont Majsuculisés
        """
        super().before_insert()
        self.alive = True


"""
champs à ajouter :
date de décès
décédé
médecin traitant déclaré
notes divers
"""


from marshmallow import Schema, fields, validate, post_load


class PatientSchema(Schema):
    nom = fields.String(required=True)
    prenom = fields.String(required=True)
    ddn = fields.Date(required=True)
    sexe = fields.String(required=True, validate=[validate.OneOf(SEXE)])
    rue = fields.String(default="")
    cp = fields.Integer(default=None, allow_null=True)
    ville = fields.String()
    tel = fields.String()
    email = fields.String()
    alive = fields.Boolean()


import hug
from falcon import HTTP_201, HTTPForbidden

# from mapistar.base_db import api


@hug.post("", status=HTTP_201)
def add(data: hug.types.MarshmallowSchema(PatientSchema())):
    """
    Ajouter un nouveau patient

    Args:
        patient: données du nouveau patient
    """

    return Patient(**data).to_dict()


@hug.get("")
def get(patientid=None):
    if patientid is None:
        return [x.to_dict() for x in Patient.select()]

    else:
        return get_or_404(Patient, patientid).to_dict()


@hug.delete("")
def delete(hug_user, patientid: hug.types.number):
    """
    delete un patient

    Args:
        id: id du patient
    Returns:
        msg "delete success"
    Raises:
        NotFound si non trouvé
    """
    pat = get_or_404(Patient, patientid)
    # if hug_user.is_admin or hug_user.permissions.del_patient:
    if True:
        pat.delete()
        return {"msg": "delete success", "patientid": patientid}
    else:
        raise HTTPForbidden(
            title=f"Action non autorisée pour l'utilisateur {hug_user.username}"
        )


@hug.put("", status=HTTP_201)
def update(
    hug_user,
    data: hug.types.MarshmallowSchema(PatientSchema(partial=True)),
    patientid: hug.types.number,
):
    """modify patients

    Args:
        new_data: Rien n'est requis.
        id: patient id.
    """
    to_update = get_or_404(db.Patient, patientid)
    to_update.set(**{k: v for k, v in data.items() if v})
    return to_update.to_dict()


# routes_patients = Include(
#     url="/patients",
#     name="patients",
#     routes=[
#         Route(url="/", method="POST", handler=add),
#         Route(url="/", method="GET", handler=liste),
#         Route(url="/{patient_id}/", method="PUT", handler=update),
#         Route(url="/{patient_id}/", method="DELETE", handler=delete),
#         Route(url="/{patient_id}/", method="GET", handler=one),
#     ],
# )
# #
