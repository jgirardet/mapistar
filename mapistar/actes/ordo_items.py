from typing import Callable

from apistar import Include, Route, http, types, validators
from pony import orm

from mapistar.base_db import db
from mapistar.exceptions import MapistarBadRequest
from mapistar.permissions import ActesPermissions
from mapistar.utils import DicoMixin, NameMixin, SetMixin


class Item(db.Entity, DicoMixin, NameMixin, SetMixin):
    ordonnance = orm.Required("Ordonnance")
    place = orm.Optional(int)

    def after_insert(self):
        self.ordonnance.before_update()  # modifief = created
        self.ordonnance.ordre_add_item(self)

    def before_delete(self):
        self.ordonnance.before_update()  # modified = datetime.utcnow()
        self.ordonnance.ordre_delete_item(self)

    def before_update(self):
        self.ordonnance.before_update()


class ItemCreateSchema(types.Type):
    """base class"""


class Medicament(Item):
    """Medicament"""
    cip = orm.Required(str)
    nom = orm.Required(str)
    posologie = orm.Optional(str)
    duree = orm.Optional(int, default=0)

    def __repr__(self):  # pragma: no cover
        return f"[Medicament: {self.nom}]"

    updatable = ("posologie", "duree")


class MedicamentCreateSchema(ItemCreateSchema):
    cip = validators.String(min_length=13)
    nom = validators.String()
    posologie = validators.String(default="")
    duree = validators.Integer(default=None, allow_null=True)


class MedicamentUpdateSchema(types.Type):
    posologie = validators.String(default="")
    duree = validators.Integer(default="")


class ItemViews:

    model = None
    schema_add = None
    schema_update = None

    @classmethod
    def add_item(cls) -> Callable:

        def add_item(data: cls.schema_add, obj: ActesPermissions):
            # obj.medicaments.create(**data)
            try:
                item = cls.model(ordonnance=obj, **data)
            except TypeError as exc:
                raise MapistarBadRequest("acte_id doit correspondre à une ordonnance")

            return http.JSONResponse(item.dico, status_code=201)

        add_item.__doc__ = f"""Ajoute un nouvel Item de type  {cls.model.name}"""
        return add_item

    @classmethod
    def delete_item(cls) -> Callable:

        def delete_item(item_id: int, obj: ActesPermissions):
            obj.delete()
            return {"id": item_id, "deleted": True}

        delete_item.__doc__ = f"""Ajoute un nouvel Item de type {cls.model.name}"""
        return delete_item

    @classmethod
    def update_item(cls) -> Callable:

        def update_item(
            item_id: int, new_data: cls.schema_update, obj: ActesPermissions
        ):
            # obj = get_or_404(cls.model, acte_id)
            obj.set(**new_data)
            return obj.dico

        update_item.__doc__ = f"""Modifie un Item de type {cls.model.name}"""
        return update_item

    @classmethod
    def routes(cls) -> Include:
        """
        Returns:
            Les routes pour chaque action
        """
        return Include(
            url=f"/{cls.model.url_name}",
            name=cls.model.url_name,
            routes=[
                Route("/add/{acte_id}", method="POST", handler=cls.add_item()),
                Route("/{item_id}/", method="DELETE", handler=cls.delete_item()),
                # Route("/{acte_id}/", method="GET", handler=cls.one()),
                Route("/{item_id}/", method="PUT", handler=cls.update_item()),
                # Route("/patient/{patient_id}/", method="GET", handler=cls.liste()),
            ],
        )


class MedicamentViews(ItemViews):
    model = Medicament
    schema_add = MedicamentCreateSchema
    schema_update = MedicamentUpdateSchema
