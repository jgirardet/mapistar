from apistar import types, validators
from collections import namedtuple
from mapistar.models import db

from apistar_cerberus import ApistarValidator
import cerberus

base_acte_schema = {"patient": {"type": "integer", "required": True}}

from collections import ChainMap

observation_schema = dict(
    ChainMap(
        base_acte_schema, {"motif": {"type": "string"}, "body": {"type": "string"}}
    )
)

ObservationCreateSchema = ApistarValidator(observation_schema)
ObservationUpdateSchema = ApistarValidator(observation_schema, update=True)
# class ObservationCreateSchema(types.Type):
#     patient = validators.Integer()
#     motif = validators.String()
#     body = validators.String(default='')

# class ObservationUpdateSchema(types.Type):
#     motif = validators.String(default='')
#     body = validators.String(default='')

SchemasCollection = namedtuple("SchemasCollection", "adder updater")

actes_schemas = {
    db.Observation: SchemasCollection(ObservationCreateSchema, ObservationUpdateSchema),
    # PrescriptionLibre:
    #     SchemasCollection(PrescriptionLibreSchema, PrescriptionLibreCreateSchema,
    #                       PrescriptionLibrUpdateSchema)
}
