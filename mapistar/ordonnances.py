from mapistar.models import db
from pony import orm
from .actes import Acte


class Ordonnance(Acte):
    pk = orm.PrimaryKey(int, auto=True)
    items = orm.Set('Item')

class Item(db.Entity):
    ordonnance = orm.Required(Ordonnance)
    place = orm.Optional(int)


class Medicament(Item):
    pass

# class Medicament(LigneOrdonnance):
#     """
#     Medicament model
#     """
#     cip = models.CharField(max_length=30)
#     nom = models.CharField(max_length=200)
#     posologie = models.CharField(max_length=200)
#     duree = models.PositiveIntegerField()  # en jours

#     def __str__(self):
# return self.nom