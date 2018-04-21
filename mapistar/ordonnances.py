# Third Party Libraries
from pony import orm

# mapistar
from mapistar.actes.models import Acte
from mapistar.models import db


class Ordonnance(Acte):
    items = orm.Set("Item")
    ordre = orm.Optional(orm.Json, default={})

    # def __init__(self, *args, **kwargs):
    #     if not "ordre" in kwargs:
    #         kwargs['ordre'] = {'ordre': ["omkm"]}
    #     super().__init__(*args, **kwargs)

    def _fait_ordre(self):
        self.ordre = {i: k.id for i, k in enumerate(self.items.select())}

    def _refait_orde_on_delete(self, deleted):
        for k, v in self.ordre.items():
            if v is deleted:
                self.ordre.pop(k)
                return

    @property
    def dico(self):
        _dico = super().dico
        _dico["items"] = [x.to_dict() for x in self.items.order_by(Item.place)]
        return _dico


# def before_insert(self):
#     if not self.ordre:
#         raise AttributeError(
#             'définition de ordre requis at instancitation')


class Item(db.Entity):
    ordonnance = orm.Required(Ordonnance)
    place = orm.Optional(int)

    def before_insert(self):
        self.place = self.ordonnance.items.count()

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
