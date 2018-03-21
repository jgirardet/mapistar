# Third Party Libraries
from apistar import typesystem


class BaseActeSchema(typesystem.Object):
    properties = {
        'id': typesystem.integer(description="Observation id"),
        'patient_id': typesystem.integer(description="Patient id"),
        'created': typesystem.string(description="Created"),
        'modified': typesystem.string(description="Last Modified"),
        'owner_id': typesystem.integer(description="owner id"),
    }
    required = []


class BaseActeCreateSchema(typesystem.Object):

    properties = {
        'patient_id': typesystem.integer(description="Patient id"),
    }
    required = ['patient_id']
