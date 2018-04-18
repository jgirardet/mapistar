from mapistar.base_db import db
from pony import orm
from descriptors import classproperty
import pendulum
from datetime import datetime
from mapistar.settings import tz
import pendulum
import pytz


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

    @property
    def created(self):
        return self._created.replace(tzinfo=pytz.utc).astimezone(tz)

    @created.setter
    def created(self, value):
        self._created = value.astimezone(pytz.utc).replace(tzinfo=None)

    @property
    def modified(self):
        return self._modified.replace(tzinfo=pytz.utc).astimezone(tz)

    @created.setter
    def modified(self, value):
        self._modified = value.astimezone(pytz.utc).replace(tzinfo=None)

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
        self._modified = datetime.utcnow()

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
