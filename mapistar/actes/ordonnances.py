# Third Party Libraries
from apistar import types, validators
from pony import orm

# mapistar
from mapistar.actes.actes import ActeCreateSchema

from .actes import Acte
from .ordo_items import Item
from .views import ActesViews


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
        """
        dico addapté aux ordonnances
        """
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
            # not first item
            if self.ordre.index(str(item_id)):
                lid = "-" + item_id
                self.ordre = self.ordre.replace(lid, "")
            # first item
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
            [self.ordre_add_item(i) for i in self.items.select()]
            return list(self.items)


class OrdonnanceCreateSchema(ActeCreateSchema):
    pass


class OrdonnanceUpdateSchema(types.Type):
    ordre = validators.String(default="")


class OrdonnanceViews(ActesViews):
    model = Ordonnance
    schema_add = OrdonnanceCreateSchema
    schema_update = OrdonnanceUpdateSchema
