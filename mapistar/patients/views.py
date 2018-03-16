# Standard Libraries
from typing import List

# Third Party Libraries
from apistar import Response
from apistar.backends.django_orm import Session
from apistar.exceptions import NotFound
from django.http import Http404
from django.shortcuts import get_object_or_404

from .schemas import PatientCreateSchema, PatientSchema, PatientUpdateSchema
from pony.orm import Database, select, desc


def patients_detail(session: Session, patient_id: int) -> PatientSchema:
    """
    Get patient details
    """
    try:
        pat = get_object_or_404(session.Patient, id=patient_id)
    except Http404 as e:
        raise NotFound(str(e))
    return PatientSchema(pat)


# class Patient(db.Entity):
#     nom = Required(str)
#     prenom = Required(str)
#     # ddn = Required(date)


def patients_create(aa: Database, patient: PatientSchema) -> Response:
    """
    create patients
    """
    # print(aa.entities)
    a = aa.Patient(
        nom=patient['nom'],
        prenom=patient['prenom'],
        ddn=patient['ddn'],
        street=patient['street'])

    # ddn=patient['birthdate'])
    # new_patient = session.Patient.objects.create(**patient)

    return Response(PatientSchema(a.to_dict()), status=201)


# def patients_create(session: Session, patient: PatientCreateSchema) -> Response:
#     """
#     create patients
#     """
#     new_patient = session.Patient.objects.create(**patient)
#     return Response(PatientSchema(new_patient), status=201)


def patients_update(session: Session, patient_id: int,
                    patient: PatientUpdateSchema) -> PatientSchema:
    """
    modify patients
    """
    a = session.Patient.objects.filter(id=patient_id).update(**patient)
    if not a:
        raise NotFound('Patient id not found')
    updated_patient = session.Patient.objects.get(id=patient_id)
    return PatientSchema(updated_patient)


def patients_list(aa: Database) -> List[PatientSchema]:
    """
    List patients
    """

    return [PatientSchema(x.to_dict()) for x in aa.Patient.select()]
