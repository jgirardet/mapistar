# Third Party Libraries
from pony import orm

# mapistar
from mapistar.actes.models import Acte
from mapistar.db import db
from mapistar.utils import DicoMixin


class Ordonnance(Acte):
    """
    Entity ORdonnance

    Attributes:
        items(mapistar.ordonnances.Item): set d'items composants l'observation
        ordre(str): Ordre des items.

    updatables:
        ordre
    """
    items = orm.Set("Item")
    ordre = orm.Optional(str, default="")

    updatable = ["ordre"]

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

    def _refait_orde_on_delete(self, deleted):
        for k, v in self.ordre.items():
            if v is deleted:
                self.ordre.pop(k)
                return

    @property
    def dico(self):
        _dico = super().dico
        _dico["items"] = [x.dico for x in self.get_ordered_items()]
        return _dico

    def get_ordered_items(self):
        if not self.ordre:
            return []
        ordre = [int(x) for x in self.ordre.split("-")]
        try:
            return sorted(list(self.items), key=lambda x: ordre.index(x.id))
        except ValueError:
            # fallback item pas dans ordre ou inversement
            return list(self.items)


class Item(db.Entity, DicoMixin):
    ordonnance = orm.Required(Ordonnance)
    place = orm.Optional(int)

    def after_insert(self):
        self.ordonnance.before_update()
        self.ordonnance.ordre_add_item(self)

    def before_delete(self):
        self.ordonnance.before_update()
        self.ordonnance.ordre_delete_item(self)

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
