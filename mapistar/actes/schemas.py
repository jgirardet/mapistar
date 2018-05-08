# Standard Libraries
from collections import namedtuple

# mapistar
from mapistar.db import db

from .observations import ObservationCreateSchema, ObservationUpdateSchema
from .ordonnances import OrdonnanceCreateSchema, OrdonnanceUpdateSchema

SchemasCollection = namedtuple("SchemasCollection", "adder updater")

actes_schemas = {
    db.Observation: SchemasCollection(ObservationCreateSchema, ObservationUpdateSchema),
    db.Ordonnance: SchemasCollection(OrdonnanceCreateSchema, OrdonnanceUpdateSchema),
    # PrescriptionLibre:
    #     SchemasCollection(PrescriptionLibreSchema, PrescriptionLibreCreateSchema,
    #                       PrescriptionLibrUpdateSchema)
}
