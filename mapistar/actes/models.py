# Standard Libraries
from datetime import datetime

# Third Party Libraries
import pendulum
from descriptors import classproperty
from pony import orm

# mapistar
from mapistar.base_db import db
from mapistar.utils import PendulumDateTime


class Acte(db.Entity):
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
    _created = orm.Required(datetime, default=datetime.utcnow)
    _modified = orm.Optional(datetime)

    @classproperty
    def name(self) -> str:
        """nom du modèle"""
        return self.__name__

    @classproperty
    def url_name(self) -> str:
        """url du modèle, utilisé dans :class:`~mapistar.actes.views.ActeViews`"""
        return self.__name__.lower() + "s"

    created = PendulumDateTime()
    modified = PendulumDateTime()

    @property
    def dico(self):
        " return to_dict but serializable"
        _dico = self.to_dict()
        [_dico.pop(x) for x in ("_created", "_modified")]
        _dico["created"] = self.created.isoformat()
        _dico["modified"] = self.modified.isoformat()
        return _dico

    def before_insert(self):
        """
        Avant insert:
            * dernière modification == création
        """
        self._modified = self._created

    def before_update(self):
        """
        Avant update:
            * dernière modification == maintenant
        """
        self.modified = pendulum.now()

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


class Observation(Acte):
    """
    Entity Observation

    Attributes:
        motif(str)*: Motif de la consultation
        body(str): Corps de lobservation
    """

    motif = orm.Required(str)
    body = orm.Optional(str)

    updatable = ("motif", "body")

    def __repr__(self):  # pragma: nocover
        return f"Observation: {self.motif} par {self.owner}"
