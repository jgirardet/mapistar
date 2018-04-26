# Third Party Libraries
from pony import orm

# mapistar
from mapistar.actes.models import Acte
from mapistar.db import db
from mapistar.utils import DicoMixin


class Ordonnance(Acte):
    items = orm.Set("Item")
    ordre = orm.Optional(str)

    # def __init__(self, *args, **kwargs):
    #     if "ordre" not in kwargs:
    #         kwargs["ordre"] = {"ordre": ["omkm"]}
    #     super().__init__(*args, **kwargs)

    def _fait_ordre(self):
        self.ordre = "-".join([str(k.id) for k in self.items.select()])
        # fmt: off
        import pdb; pdb.set_trace() # fmt: on
        print(self.ordre)

    def _refait_orde_on_delete(self, deleted):
        for k, v in self.ordre.items():
            if v is deleted:
                self.ordre.pop(k)
                return

    @property
    def dico(self):
        _dico = super().dico
        _dico["items"] = [x.dico for x in self.items.order_by(Item.place)]
        return _dico


# def before_insert(self):
#     if not self.ordre:
#         raise AttributeError(
#             'définition de ordre requis at instancitation')


class Item(db.Entity, DicoMixin):
    ordonnance = orm.Required(Ordonnance)
    place = orm.Optional(int)

    def before_insert(self):
        self.place = self.ordonnance.items.count()
        self.ordonnance._fait_ordre()

    def after_insert(self):
        # self.ordonnance.ordre.append(self.id)
        self.ordonnance.before_update()

    def before_delete(self):
        self.ordonnance.before_update()

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
