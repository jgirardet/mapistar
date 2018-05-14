# Standard Libraries
from typing import Callable, List

# Third Party Libraries
from apistar import Include, Route, http
from apistar_jwt.token import JWTUser

# mapistar
# from mapistar.db import db
from mapistar.permissions import ActesPermissions
from mapistar.utils import get_or_404
from pony.orm import select


class ActesViews:
    """
    class factory pour les actes.

    Les handlers et les routes sont fabriquées à la volée.
    Fournit add, liste, delete, update, one.

    Args:
        model: modèle pony, hérité de :class:`BaseActe`
        schema_add: schema utilisé pour la création d'un acte
        schema_updat: schema utilisé pour la mise à jour d'un acte

    Returns:
        Une liste d'URL
    """

    model = None
    schema_add = None
    schema_update = None

    @classmethod
    def add(cls) -> Callable:

        def add(data: cls.schema_add, user: JWTUser) -> http.JSONResponse:
            obj = cls.model(owner=user.id, **data)
            return http.JSONResponse(obj.dico, status_code=201)

        add.__doc__ = f"""Ajoute un nouvel Acte de type {cls.model.name}"""

        return add

    @classmethod
    def liste(cls) -> Callable:

        def liste(patient_id: int) -> List:
            # fmt: off
            return [
                acte.dico for acte in select(a for a in cls.model if a.patient.id == patient_id)
            ]
            # fmt: on

        liste.__doc__ = f""" Liste les Actes de type {cls.model.name}"""
        return liste

    @classmethod
    def one(cls) -> Callable:

        def one(acte_id: int) -> dict:
            obj = get_or_404(cls.model, acte_id)
            return obj.dico

        one.__doc__ = f"""Accède à un Acte de type {cls.model.name}"""
        return one

    @classmethod
    def delete(cls) -> Callable:

        def delete(acte_id: int, obj: ActesPermissions) -> dict:
            obj.delete()
            return {"id": acte_id, "deleted": True}

        delete.__doc__ = f"""Efface un Acte de type {cls.model.name}"""
        return delete

    @classmethod
    def update(cls) -> Callable:

        def update(acte_id: int, new_data: cls.schema_update, obj: ActesPermissions):
            # obj = get_or_404(cls.model, acte_id)
            obj.set(**new_data)
            return obj.dico

        update.__doc__ = f"""Modifie un acte de type {cls.model.name}"""
        return update

    @classmethod
    def routes_supplementaires(cls):
        return []

    @classmethod
    def do_routes(cls) -> Include:
        """
        Returns:
            Include: Les routes pour chaque action
        """

        bases_routes = [
            Route("/", method="POST", handler=cls.add()),
            Route("/{acte_id}/", method="GET", handler=cls.one()),
            Route("/{acte_id}/", method="DELETE", handler=cls.delete()),
            Route("/{acte_id}/", method="PUT", handler=cls.update()),
            Route("/patient/{patient_id}/", method="GET", handler=cls.liste()),
        ]

        routes = [*bases_routes, *cls.routes_supplementaires()]

        return Include(
            url=f"/{cls.model.url_name}", name=cls.model.url_name, routes=routes
        )
