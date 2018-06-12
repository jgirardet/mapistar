# Third Party Libraries
from apistar import types, validators
from pony import orm

# mapistar
from mapistar.actes.actes import ActeCreateSchema

from .actes import Acte
from .views import ActesViews

from mapistar.annuaire import Praticien


class Avis(Acte):
    """
    Entity Avis

    Regroupe les courriers reçu des confrères

    Attributes:
    """

    praticien = orm.Optional(Praticien)
