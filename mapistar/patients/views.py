# Standard Libraries
from typing import List

# Third Party Libraries
from apistar.exceptions import NotFound

from .schemas import PatientSchema
from pony.orm import Database, select, desc, db_session

from mapistar.models import db
from apistar import http


@db_session
def patients_create(patient: PatientSchema, aaa: int = 0) -> http.Response:
    """
    create patients
    """
    # print(aa.entities)
    a = db.Patient(**patient)
    print('mkoooooooooo: ', aaa)
    # ddn=patient['birthdate'])
    # new_patient = session.Patient.objects.create(**patient)

    return http.Response(PatientSchema(a.to_dict()), status_code=201)


def aaa() -> http.Response:
    """
    create patients
    """
    # print(aa.entities)
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

    return http.Response({"hello": "HELLO"}, status_code=201)


# def patients_detail(session: Session, patient_id: int) -> PatientSchema:
#     """
#     Get patient details
#     """
#     try:
#         pat = get_object_or_404(session.Patient, id=patient_id)
#     except Http404 as e:
#         raise NotFound(str(e))
#     return PatientSchema(pat)

# def patients_create(aa: Database, patient: PatientSchema) -> Response:
#     """
#     create patients
#     """
#     # print(aa.entities)
#     a = aa.Patient(
#         nom=patient['nom'],
#         prenom=patient['prenom'],
#         ddn=patient['ddn'],
#         street=patient['street'])

#     # ddn=patient['birthdate'])
#     # new_patient = session.Patient.objects.create(**patient)

#     return Response(PatientSchema(a.to_dict()), status=201)

# # def patients_create(session: Session, patient: PatientCreateSchema) -> Response:
# #     """
# #     create patients
# #     """
# #     new_patient = session.Patient.objects.create(**patient)
# #     return Response(PatientSchema(new_patient), status=201)

# def patients_update(session: Session, patient_id: int,
#                     patient: PatientUpdateSchema) -> PatientSchema:
#     """
#     modify patients
#     """
#     a = session.Patient.objects.filter(id=patient_id).update(**patient)
#     if not a:
#         raise NotFound('Patient id not found')
#     updated_patient = session.Patient.objects.get(id=patient_id)
#     return PatientSchema(updated_patient)

# def patients_list(aa: Database) -> List[PatientSchema]:
#     """
#     List patients
#     """

#     return [PatientSchema(x.to_dict()) for x in aa.Patient.select()]
