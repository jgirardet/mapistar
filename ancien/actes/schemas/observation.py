# Third Party Libraries
from apistar import typesystem

from .base import BaseActeCreateSchema, BaseActeSchema


class ObservationSchema(typesystem.Object):
    new_properties = {
        'motif': typesystem.string(description="Motif"),
        'body': typesystem.string(description="Texte de l'observation"),
    }
    properties = dict(BaseActeSchema.properties, **new_properties)
    required = []


class ObservationCreateSchema(typesystem.Object):
    """"
    ObservationCreateSchema

    """
    new_properties = {
        'motif': typesystem.string(max_length=60, description="Motif"),
        'body': typesystem.string(description="Texte de l'observation"),
    }
    properties = dict(BaseActeCreateSchema.properties, **new_properties)
    required = BaseActeCreateSchema.required + ['motif']


class ObservationUpdateSchema(typesystem.Object):
    """
    Update only-schema
    """
    properties = {
        'motif': typesystem.string(max_length=60, description="Motif"),
        'body': typesystem.string(description="Texte de l'observation"),
    }
    # properties = ObservationCreateSchema.new_properties
    required = []
