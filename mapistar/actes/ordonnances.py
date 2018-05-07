# Third Party Libraries
from pony import orm

# mapistar
from mapistar.db import db
from mapistar.utils import DicoMixin

from .actes import Acte
from apistar import validators, types
from .ordo_items import Item


class Ordonnance(Acte):
    """
    Entity ORdonnance

    Attributes:
        items(mapistar.ordonnances.Item): set d'items composants l'observation
        ordre(str): Ordre des items.

    updatables:
        ordre
    """
    items = orm.Set(Item)
    ordre = orm.Optional(str, default="")

    updatable = ["ordre"]

    @property
    def dico(self):
        _dico = super().dico
        _dico["items"] = [x.dico for x in self.get_ordered_items()]
        return _dico

    def ordre_add_item(self, item: "Item"):
        if not self.ordre:
            self.ordre += f"{item.id}"
        else:
            self.ordre += f"-{item.id}"

    def ordre_delete_item(self, item: "Item"):
        if "-" in self.ordre:
            lid = "-" + f"{item.id}"
            # print(lid)
            # print(item.id, self.ordre, self.items.select()[:])
            self.ordre = self.ordre.replace(lid, "")
        else:
            self.ordre = ""

    def get_ordered_items(self):
        if not self.ordre:
            return []

        ordre = [int(x) for x in self.ordre.split("-")]
        try:
            return sorted(list(self.items), key=lambda x: ordre.index(x.id))

        except ValueError:
            # fallback item pas dans ordre ou inversement
            return list(self.items)


class OrdonnanceCreateSchema(types.Type):
    patient = validators.Integer()


class OrdonnanceUpdateSchema(types.Type):
    ordre = validators.String(default="")


# Views
