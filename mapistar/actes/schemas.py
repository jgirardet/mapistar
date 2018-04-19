# Standard Libraries
from collections import namedtuple

# Third Party Libraries
from apistar import types, validators

# mapistar
from mapistar.models import db


class ObservationCreateSchema(types.Type):
    motif = validators.String()
    body = validators.String(default="")


class ObservationUpdateSchema(types.Type):

    motif = validators.String(default="")
    body = validators.String(default="")


SchemasCollection = namedtuple("SchemasCollection", "adder updater")

actes_schemas = {
    db.Observation: SchemasCollection(ObservationCreateSchema, ObservationUpdateSchema),
    # PrescriptionLibre:
    #     SchemasCollection(PrescriptionLibreSchema, PrescriptionLibreCreateSchema,
    #                       PrescriptionLibrUpdateSchema)
}
