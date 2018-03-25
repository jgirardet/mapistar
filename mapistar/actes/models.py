from mapistar.models import db
from pony import orm
from datetime import datetime


class Acte(db.Entity):
    """
    Base class for for differnets actions
    made by users
    Updatable fields by user must be set in updatable
    """
    pk = orm.PrimaryKey(int, auto=True)
    patient = orm.Required('Patient')
    owner = orm.Required('User')
    created = orm.Required(datetime, default=datetime.now())
    modified = orm.Optional(datetime)

    @property
    def dico(self):
        " return to_dict but serializable"
        _dico = self.to_dict()
        _dico['created'] = _dico['created'].isoformat()
        _dico['modified'] = _dico['modified'].isoformat()
        return _dico

    def before_insert(self):
        self.modified = self.created

    def before_update(self):
        self.modified = datetime.now()

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

    def __repr__(self):
        return f"Observation: {self.motif} par {self.owner}"

    url_name = "observations"
