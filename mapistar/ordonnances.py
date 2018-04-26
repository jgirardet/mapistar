# Third Party Libraries
from pony import orm

# mapistar
from mapistar.actes.models import Acte
from mapistar.db import db
from mapistar.utils import DicoMixin


class Ordonnance(Acte):
    items = orm.Set("Item")
    ordre = orm.Optional(str, default="")
    duree = orm.Optional(int)
    oar = orm.Optional(int)

    def get_ordered_items(self):
        items = []
        for it in self.ordre.strip("-").split("-"):
            items.append(db.Item[it])
        return items

    @property
    def dico(self):
        _dico = super().dico
        _dico["items"] = [x.dico for x in self.get_ordered_items()]
        return _dico


# def before_insert(self):
#     if not self.ordre:
#         raise AttributeError(
#             'définition de ordre requis at instancitation')


class Item(db.Entity, DicoMixin):
    ordonnance = orm.Required(Ordonnance)

    def before_insert(self):
        self.place = self.ordonnance.items.count()

    def after_insert(self):
        self.ordonnance.before_update()
        self.ordonnance.ordre += f"-{self.id}"

    def before_delete(self):
        self.ordonnance.before_update()
        self.ordonnance.ordre = self.ordonnance.ordre.replace(f"-{self.id}", "")

    def before_update(self):
        self.ordonnance.before_update()


class Medicament(Item):
    """Medicament"""
    cip = orm.Required(str)
    nom = orm.Required(str)
    posologie = orm.Optional(str)
    duree = orm.Optional(int, default=0)

    def __repr__(self):
        return f"[{self.nom}]"
