# Standard Libraries
from typing import List

# Third Party Libraries
from apistar import http
from apistar.exceptions import BadRequest
from pony.orm import db_session

# mapistar
from mapistar.models import db
from mapistar.utils.shortcuts import get_or_404

from .schemas import PatientSchema, PatientUpdateSchema


@db_session
def add(patient: PatientSchema) -> http.Response:
    """
    create patients
    """
    if 'pk' is not None in patient:
        raise BadRequest("pk ne peut être spédicifée pour un ajout")

    print(patient)
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
