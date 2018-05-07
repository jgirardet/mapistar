from mapistar.base_db import db
from pony import orm
from mapistar.utils import DicoMixin, NameMixin
from apistar import validators, types


class Item(db.Entity, DicoMixin, NameMixin):
    ordonnance = orm.Required("Ordonnance")
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


class MedicamentCreateSchema(types.Type):
    ordonnance = validators.Integer()
    cip = validators.String(min_length=13)
    nom = validators.String()
    posologie = validators.String(default="")
    duree = validators.Integer(default=None, allow_null=True)


class MedicamentUpdateSchema(types.Type):
    posologie = validators.String(default="")
    duree = validators.Integer(default="")


from typing import Callable, List
from apistar_jwt import JWTUser
from apistar import http, Include, Route


class ItemViews:

    model = None
    schema_add = None
    schema_update = None

    @classmethod
    def add(self) -> Callable:

        def add(data: self.schema_add, user: JWTUser) -> http.JSONResponse:
            obj = self.model(**data)
            return http.JSONResponse(obj.dico, status_code=201)

        add.__doc__ = f"""Ajoute un nouvel Item de type : {self.model.name}"""
        return add

    @classmethod
    def routes(self) -> Include:
        """
        Returns:
            Les routes pour chaque action
        """
        print(self.model.name, self.model.url_name)
        return Include(
            url=f"/{self.model.url_name}",
            name=self.model.url_name,
            routes=[
                Route("/", method="POST", handler=self.add()),
                # Route("/{acte_id}/", method="GET", handler=self.one()),
                # Route("/{acte_id}/", method="DELETE", handler=self.delete()),
                # Route("/{acte_id}/", method="PUT", handler=self.update()),
                # Route("/patient/{patient_id}/", method="GET", handler=self.liste()),
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
