# Standard Libraries
from typing import List

# Third Party Libraries
from apistar.exceptions import NotFound, BadRequest

from .schemas import PatientSchema
from pony.orm import Database, select, desc, db_session

from mapistar.models import db
from apistar import http
from mapistar.utils.shortcuts import get_or_404


@db_session
def add(patient: PatientSchema) -> http.Response:
    """
    create patients
    """
    if 'pk' is not None in patient:
        raise BadRequest("pk ne peut être spédicifée pour un ajout")

    a = db.Patient(**patient)
    return http.Response(PatientSchema(a.to_dict()), status_code=201)


@db_session
def liste() -> List[PatientSchema]:
    """ List patients """
    return [PatientSchema(x.to_dict()) for x in db.Patient.select()]


@db_session
def get(patient_pk: int) -> PatientSchema:
    """ Get patient details """
    pat = get_or_404(db.Patient, patient_pk)
    return PatientSchema(pat)


@db_session
def delete(patient_pk: int) -> dict:
    """delete un patient"""
    pat = get_or_404(db.Patient, patient_pk)
    pat.delete()
    return {"msg": "delete success"}


def update(new_data: PatientSchema) -> PatientSchema:
    """ modify patients """
    if 'pk' is None:
        raise BadRequest('la pk doit être spédicifée')
    to_update = get_or_404(new_data['pk'])
    to_update.set(**new_data)
    return PatientSchema(to_update.to_dict())
