from apistar import types, validators
from collections import namedtuple
from mapistar.models import db


class ObservationCreateSchema(types.Type):
    patient = validators.Integer()
    motif = validators.String()
    body = validators.String(default='')


class ObservationUpdateSchema(types.Type):
    motif = validators.String()
    body = validators.String(default='')


SchemasCollection = namedtuple('SchemasCollection', 'adder updater')

actes_schemas = {
    db.Observation:
    SchemasCollection(ObservationCreateSchema, ObservationUpdateSchema),
    # PrescriptionLibre:
    #     SchemasCollection(PrescriptionLibreSchema, PrescriptionLibreCreateSchema,
    #                       PrescriptionLibrUpdateSchema)
}
