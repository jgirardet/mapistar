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
    Base class for for differnets actions
    made by users
    Updatable fields by user must be set in updatable
    """
    pk = orm.PrimaryKey(int, auto=True)
    patient = orm.Required("Patient")
    owner = orm.Required("User")
    _created = orm.Required(datetime, default=datetime.utcnow)
    _modified = orm.Optional(datetime)

    @classproperty
    def url_name(self):
        return self.__name__.lower() + "s"

    @classproperty
    def name(self):
        return self.__name__.lower() + "s"

    created = PendulumDateTime()
    modified = PendulumDateTime()

    @property
    def dico(self):
        " return to_dict but serializable"
        _dico = self.to_dict()
        del _dico["_created"]
        del _dico["_modified"]
        _dico["created"] = self.created.isoformat()
        _dico["modified"] = self.modified.isoformat()
        return _dico

    def before_insert(self):
        self._modified = self._created

    # pass

    def before_update(self):
        self.modified = pendulum.now()

    updatable = ()

    def set(self, **kwargs):
        """ override default set pour vérifier si updatable"""
        for item in kwargs:
            if item not in self.updatable:
                raise AttributeError(f"{item} n'est pas updatable")

        super().set(**kwargs)


class Observation(Acte):
    motif = orm.Required(str)
    body = orm.Optional(str)

    updatable = ("motif", "body")

    def __repr__(self):  # pragma: nocover
        return f"Observation: {self.motif} par {self.owner}"
