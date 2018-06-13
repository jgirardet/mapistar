# Standard Libraries
from datetime import datetime

# Third Party Libraries
from apistar import types, validators
from pony import orm

# mapistar
from mapistar.base_db import db
from mapistar.utils import DicoMixin, NameMixin, SetMixin


class Acte(DicoMixin, NameMixin, SetMixin, db.Entity):
    """
    Base Entity pour les différents actes.

    Les fields updatables sont spécifiés dans updatable

    Attributes:
        patient(mapistar.Patient): Patient
        owner(mapistar.User): Créateur de l'Acte
        created: date de création
        modified: dernière modification


    """

    patient = orm.Required("Patient")
    owner = orm.Required("User")
    created = orm.Required(datetime, default=datetime.utcnow)
    modified = orm.Optional(datetime)
    pj = orm.Set('Document')

    def before_insert(self):
        """
        Avant insert:
            * dernière modification == création
        """
        self.modified = self.created

    def before_update(self):
        """
        Avant update:
            * dernière modification == maintenant
        """
        self.modified = datetime.utcnow()

    updatable = ()
    """updatable définie les attributs pouvant être mis à jours
    via la fonction set
    """


class ActeCreateSchema(types.Type):
    patient = validators.Integer()
