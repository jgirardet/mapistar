# Third Party Libraries
from apistar import Include, Route, http
from apistar_jwt.token import JWTUser
from mapistar.db import db
from mapistar.permissions import ActesPermissions
from mapistar.utils import get_or_404
from typing import List, Callable

from .schemas import actes_schemas


class ActesViews:
    """
    class factory pour les actes.

    Les handlers et les routes sont fabriquées à la volée.
    Fournit add, liste, delete, update, one.

    Args:
        model: modèle pony, hérité de :class:`BaseActe`
    
    Returns:
        Une liste d'URL
    """

    def __init__(self, model: db.Entity):
        # model needed as key for schemas and parameter  for permissions
        self.model = model
        self.schemas = actes_schemas[model]

    def add(self) -> Callable:

        def add(data: self.schemas.adder, user: JWTUser) -> http.JSONResponse:
            obj = self.model(owner=user.id, **data)
            return http.JSONResponse(obj.dico, status_code=201)

        add.__doc__ = f"""Ajoute un nouvel Acte de type : {self.model.name}"""
        return add

    def liste(self) -> Callable:

        def liste(patient_id: int) -> List:
            return [  # pragma: nocover
                acte.dico
                for acte in self.model.select(lambda a: a.patient.id == patient_id)
            ]

        liste.__doc__ = f""" Liste les Actes de type : {self.model.name}"""
        return liste

    def one(self) -> Callable:

        def one(acte_id: int) -> dict:
            obj = get_or_404(self.model, acte_id)
            return obj.dico

        one.__doc__ = f"""Accède à un Acte de type : {self.model.name}"""
        return one

    def delete(self) -> Callable:

        def delete(acte_id: int, obj: ActesPermissions) -> dict:
            # obj = get_or_404(self.model, acte_id)
            obj.delete()
            return {"id": acte_id, "deleted": True}

        delete.__doc__ = f"""Efface un Acte de type : {self.model.name}"""
        return delete

    def update(self) -> Callable:

        def update(acte_id: int, new_data: self.schemas.updater, obj: ActesPermissions):
            # obj = get_or_404(self.model, acte_id)
            obj.set(**new_data)
            return obj.dico

        update.__doc__ = f"""Modifie un acte de type : {self.model.name}"""
        return update

    def __call__(self) -> Include:
        """
        Returns:
            Les routes pour chaque action
        """
        return Include(
            url=f"/{self.model.url_name}",
            name=self.model.url_name,
            routes=[
                Route("/", method="POST", handler=self.add()),
                Route("/{acte_id}/", method="GET", handler=self.one()),
                Route("/{acte_id}/", method="DELETE", handler=self.delete()),
                Route("/{acte_id}/", method="PUT", handler=self.update()),
                Route("/patient/{patient_id}/", method="GET", handler=self.liste()),
            ],
        )


routes_observations = ActesViews(db.Observation)()
