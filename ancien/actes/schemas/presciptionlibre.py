# Third Party Libraries
from apistar import typesystem

from .base import BaseActeCreateSchema, BaseActeSchema


class PrescriptionLibreSchema(typesystem.Object):
    new_properties = {
        'titre': typesystem.string(description="titre"),
        'body': typesystem.string(description="Texte de prescription"),
    }
    properties = dict(BaseActeSchema.properties, **new_properties)
    required = []


class PrescriptionLibreCreateSchema(typesystem.Object):
    """"
    PresciptionLibrecreate

    """
    new_properties = {
        'titre': typesystem.string(max_length=60, description="titre"),
        'body': typesystem.string(description="Texte de prescription"),
    }
    properties = dict(BaseActeCreateSchema.properties, **new_properties)
    required = BaseActeCreateSchema.required + ['titre']


class PrescriptionLibrUpdateSchema(typesystem.Object):
    """
    Update only-schema
    """
    properties = {
        'titre': typesystem.string(max_length=60, description="titre"),
        'body': typesystem.string(description="Texte de prescription"),
    }
    # properties = ObservationCreateSchema.new_properties
    required = []
