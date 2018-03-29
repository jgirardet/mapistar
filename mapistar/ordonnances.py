from mapistar.models import db
from pony import orm
from .actes import Acte
from pony import orm
from datetime import datetime
import pendulum


class Ordonnance(Acte):
    items = orm.Set('Item')

    def update(self):
        self.modified = pendulum.utcnow()

    @property
    def dico(self):
        _dico = super().dico
        _dico['items'] = [x.to_dict() for x in self.items.order_by(Item.place)]
        return _dico


class Item(db.Entity):
    ordonnance = orm.Required(Ordonnance)
    place = orm.Optional(int)

    def before_insert(self):
        self.place = self.ordonnance.items.count()

    def after_insert(self):
        self.ordonnance.update()

    def before_delete(self):
        self.ordonnance.update()

    def after_update(self):
        self.ordonnance.update()


class Medicament(Item):
    """Medicament"""
    cip = orm.Required(int)
    nom = orm.Required(str)
    posologie = orm.Optional(str)
    duree = orm.Optional(int, default=0)

    def __repr__(self):
        return f"[{self.nom}]"


# class Medicament(LigneOrdonnance):
#     """
#     Medicament model
#     """
#     cip = models.CharField(max_length=30)
#     nom = models.CharField(max_length=200)
#     posologie = models.CharField(max_length=200)
#     duree = models.PositiveIntegerField()  # en jours

#     def __str__(self):
#      return self.nom