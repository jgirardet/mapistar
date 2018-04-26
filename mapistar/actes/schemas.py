# Standard Libraries
from collections import namedtuple

# Third Party Libraries
from apistar import types, validators

# mapistar
from mapistar.db import db


class ObservationCreateSchema(types.Type):
    patient = validators.Integer()
    motif = validators.String()
    body = validators.String(default="")


class ObservationUpdateSchema(types.Type):

    motif = validators.String(default="")
    body = validators.String(default="")


class OrdonnanceCreateSchema(types.Type):
    patient = validators.Integer()


class OrdonnanceUpdateSchema(types.Type):
    ordre = validators.String()
    duree = validators.Integer()
    oar = validators.Integer()


class MedicamentCreateSchema(types.Type):
    ordonnance = validators.Integer()
    cip = validators.Integer()
    nom = validators.String()
    posologie = validators.String()
    duree = validators.String()


SchemasCollection = namedtuple("SchemasCollection", "adder updater")

actes_schemas = {
    db.Observation: SchemasCollection(ObservationCreateSchema, ObservationUpdateSchema),
    db.Ordonnance: SchemasCollection(OrdonnanceCreateSchema, OrdonnanceUpdateSchema),
    # PrescriptionLibre:
    #     SchemasCollection(PrescriptionLibreSchema, PrescriptionLibreCreateSchema,
    #                       PrescriptionLibrUpdateSchema)
}
