# Third Party Libraries
from apistar import types, validators
from pony import orm

from .actes import Acte
from .ordo_items import Item

from .ordo_items import MedicamentCreateSchema, MedicamentUpdateSchema


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
        item_id = str(item.id)
        # many item
        if "-" in self.ordre:
            if self.ordre.index(str(item_id)):
                lid = "-" + item_id
                self.ordre = self.ordre.replace(lid, "")
            else:
                lid = item_id + "-"
                self.ordre = self.ordre.replace(lid, "")
        # one item left
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


from .views import ActesViews


class OrdonnanceViews(ActesViews):
    model = Ordonnance
    schema_add = OrdonnanceCreateSchema
    schema_update = OrdonnanceUpdateSchema
