# Standard Libraries
from typing import Callable, List

# Third Party Libraries
from apistar import Include, Route, http, types, validators
from apistar_jwt import JWTUser
from pony import orm

# mapistar
from mapistar.base_db import db
from mapistar.utils import DicoMixin, NameMixin


class Item(db.Entity, DicoMixin, NameMixin):
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


class Medicament(Item):
    """Medicament"""
    cip = orm.Required(str)
    nom = orm.Required(str)
    posologie = orm.Optional(str)
    duree = orm.Optional(int, default=0)

    def __repr__(self):
        return f"[{self.nom}]"


class MedicamentCreateSchema(types.Type):
    ordonnance = validators.Integer()
    cip = validators.String(min_length=13)
    nom = validators.String()
    posologie = validators.String(default="")
    duree = validators.Integer(default=None, allow_null=True)


class MedicamentUpdateSchema(types.Type):
    posologie = validators.String(default="")
    duree = validators.Integer(default="")


# from mapistar.base_db import db

# from apistar import Route, http
from mapistar.permissions import ActesPermissions


# def update_item(acte_id: int, new_data: MedicamentCreateSchema, obj: ActesPermissions):
#     # obj = get_or_404(cls.model, acte_id)
#     obj.set(**new_data)
#     return obj.dico


#     @classmethod
#     def routes_supplementaires(cls):
#         return [
#             Route("/{ordonnance_id}/", method="POST", handler=add_item),
#             Route("/{acte_id}/item/{item_id}/", method="DELETE", handler=delete_item),
#         ]


class ItemViews:

    model = None
    schema_add = None
    schema_update = None

    @classmethod
    def add_item(cls) -> Callable:

        def add_item(data: cls.schema_add):
            item = cls.model(**data)
            return http.JSONResponse(item.dico, status_code=201)

        add_item.__doc__ = f"""Ajoute un nouvel Item de type : {cls.model.name}"""
        return add_item

    @classmethod
    def delete_item(cls) -> Callable:

        def delete_item(item_id: int, obj: ActesPermissions):
            obj.delete()
            return {"id": item_id, "deleted": True}

        delete_item.__doc__ = f"""Ajoute un nouvel Item de type : {cls.model.name}"""
        return delete_item

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
                Route("/", method="POST", handler=cls.add_item()),
                Route("/{item_id}/", method="DELETE", handler=cls.delete_item()),
                # Route("/{acte_id}/", method="GET", handler=cls.one()),
                # Route("/{acte_id}/", method="DELETE", handler=cls.delete()),
                # Route("/{acte_id}/", method="PUT", handler=cls.update()),
                # Route("/patient/{patient_id}/", method="GET", handler=cls.liste()),
            ],
        )


class MedicamentViews(ItemViews):
    model = Medicament
    schema_add = MedicamentCreateSchema
    schema_update = MedicamentUpdateSchema


# def add(patient: PatientCreateSchema) -> http.JSONResponse:
#     """
#     Ajouter un nouveau patient

#     Args:
#         patient: données du nouveau patient
#     """
#     a = db.Patient(**patient)
#     return http.JSONResponse(a.dico, status_code=201)


# def liste() -> List[dict]:
#     """ List patients

#     Returns:
#         Liste de tous les patients
#     """
#     return [x.dico for x in db.Patient.select()]


# def get(id: int) -> dict:
#     """ Get patient details

#     Args:
#         id: id du patient

#     Returns:
#         Le patient
#     Raises:
#         NotFound si non trouvé.
#     """
#     return get_or_404(db.Patient, id).dico


# def delete(id: int) -> dict:
#     """
#     delete un patient

#     Args:
#         id: id du patient
#     Returns:
#         msg "delete success"
#     Raises:
#         NotFound si non trouvé
#     """
#     pat = get_or_404(db.Patient, id)
#     pat.delete()
#     return {"msg": "delete success"}


# def update(new_data: PatientUpdateSchema, id: int) -> http.JSONResponse:
#     """modify patients

#     Args:
#         new_data: Rien n'est requis.
#         id: patient id.
#     """
#     to_update = get_or_404(db.Patient, id)
#     to_update.set(**{k: v for k, v in new_data.items() if v})
#     return http.JSONResponse(to_update.dico, status_code=201)


# routes_patients = Include(
#     url="/patients",
#     name="patients",
#     routes=[
#         Route(url="/", method="POST", handler=add),
#         Route(url="/", method="GET", handler=liste),
#         Route(url="/{id}/", method="PUT", handler=update),
#         Route(url="/{id}/", method="DELETE", handler=delete),
#         Route(url="/{id}/", method="GET", handler=get),
#     ],
# )
