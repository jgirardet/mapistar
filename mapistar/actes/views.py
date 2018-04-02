from pony import orm
from .schemas import ObservationCreateSchema
from mapistar.models import db
from apistar import http
from apistar import Route, http, Include

from .schemas import actes_schemas

from typing import List
from mapistar.shortcuts import get_or_404


class ActesViews:
    def __init__(self, model):
        # model needed as key for schemas and parameter  for permissions
        self.model = model
        self.schemas = actes_schemas[model]

    def add(self):
        @orm.db_session
        def add(new_obs: self.schemas.adder) -> http.Response:
            a = dict(new_obs)
            b = db.User.create_user('j', 'j', 'nom', 'prenom')
            a['owner'] = b
            obs = db.Observation(**a)
            return http.JSONResponse(obs.dico, status_code=201)

        add.__doc__ = f"""Ajoute un nouvel Acte de type : {self.model.name}"""
        return add

    def liste(self):
        @orm.db_session
        def liste(patient_pk: int) -> List:
            return [
                acte.dico for acte in self.model.select(
                    lambda a: a.patient.pk == patient_pk)
            ]

        liste.__doc__ = f""" Liste les Actes de type : {self.model.name}"""
        return liste

    def one(self):
        @orm.db_session
        def one(acte_pk: int) -> dict:
            obj = get_or_404(self.model, acte_pk)
            return obj.dico

        one.__doc__ = f"""Accède à un Acte de type : {self.model.name}"""
        return one

    def delete(self):
        @orm.db_session
        def delete(acte_pk: int) -> dict:
            obj = get_or_404(self.model, acte_pk)
            obj.delete()
            return {'pk': acte_pk, "deleted": True}

        delete.__doc__ = f"""Efface un Acte de type : {self.model.name}"""
        return delete

    def update(self):
        @orm.db_session
        def update(acte_pk: int, new_data: self.schemas.updater):
            obj = get_or_404(self.model, acte_pk)
            obj.set(**new_data)
            return obj.dico

        update.__doc__ = f"""Modifie un acte de type : {self.model.name}"""
        return update

    def urls(self):
        return Include(
            url=f'/{self.model.url_name}',
            name=self.model.url_name,
            routes=[
                Route('/', method='POST', handler=self.add()),
                Route('/{acte_pk}/', method='GET', handler=self.one()),
                Route('/{acte_pk}/', method='DELETE', handler=self.delete()),
                Route('/{acte_pk}/', method='PUT', handler=self.update()),
                Route(
                    '/patient/{patient_pk}/',
                    method='GET',
                    handler=self.liste()),
            ])