# Third Party Libraries
from apistar import types, validators
from pony import orm

from .actes import Acte, ActeCreateSchema


class Observation(Acte):
    """
    Entity Observation

    Attributes:
        motif(str)*: Motif de la consultation
        body(str): Corps de lobservation

    updatables:
        motif, body
    """

    motif = orm.Required(str)
    body = orm.Optional(str)

    updatable = ("motif", "body")

    def __repr__(self):  # pragma: nocover
        return f"Observation: {self.motif} par {self.owner}"


class ObservationCreateSchema(ActeCreateSchema):
    motif = validators.String()
    body = validators.String(default="")


class ObservationUpdateSchema(types.Type):

    motif = validators.String(default="")
    body = validators.String(default="")


from .views import ActesViews


class ObservationViews(ActesViews):
    model = Observation
    schema_add = ObservationCreateSchema
    schema_update = ObservationUpdateSchema
