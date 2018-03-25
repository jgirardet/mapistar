from pony import orm
from .schemas import ObservationCreateSchema
from mapistar.models import db
from apistar import http
from apistar import Route, http, Include

from .schemas import actes_schemas


def add(new_obs: ObservationCreateSchema):
    a = dict(new_obs)
    a['owner'] = 1
    obs = db.Observation(**a)
    return http.Response(obs.dico, status_code=201)


class ActesViews:
    def __init__(self, model):
        # model needed as key for schemas and parameter  for permissions
        self.model = model

    def add(self):
        def add(new_obs: actes_schemas[self.model].adder) -> http.Response:
            a = dict(new_obs)
            a['owner'] = 1
            obs = db.Observation(**a)
            return http.Response(obs.dico, status_code=201)

        add.__doc__ = f""" Create a new {self.model.name}"""
        print(add.__doc__)
        return add

    def urls(self):
        return Include(
            url=f'/{self.model.url_name}',
            name=self.model.url_name,
            routes=[
                Route(f'/', method='POST', handler=self.add()),
            ])