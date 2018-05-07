# Standard Libraries
from datetime import datetime

# Third Party Libraries
from pony import orm

# mapistar
from mapistar.base_db import db
from mapistar.utils import DicoMixin, NameMixin


class Acte(db.Entity, DicoMixin, NameMixin):
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

    def set(self, **kwargs: dict):
        """
        Override default set pour vérifier si updatable

        Args:
            kwargs: field : nouvelle valeur

        Raises:
            AttributeError: si le field n'est pas dans :attr:`updatable`.
        """
        for item in kwargs:
            if item not in self.updatable:
                raise AttributeError(f"{item} n'est pas updatable")

        super().set(**kwargs)
