from collections import namedtuple

from .observation import ObservationSchema, ObservationCreateSchema, ObservationUpdateSchema
from .presciptionlibre import PrescriptionLibreSchema, PrescriptionLibreCreateSchema, PrescriptionLibrUpdateSchema

from actes.models import Observation, PrescriptionLibre

SchemasCollection = namedtuple('SchemasCollection', 'getter creater updater')

actes_schemas = {
    Observation:
        SchemasCollection(ObservationSchema, ObservationCreateSchema, ObservationUpdateSchema),
    PrescriptionLibre:
        SchemasCollection(PrescriptionLibreSchema, PrescriptionLibreCreateSchema,
                          PrescriptionLibrUpdateSchema)
}
