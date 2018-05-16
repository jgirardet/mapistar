from apistar import App
from apistar_jwt.token import JWT
from apistar_ponyorm import PonyDBSession
from simple_settings import settings

from mapistar.actes.routes import (
    routes_medicaments,
    routes_observations,
    routes_ordonnances,
)
from mapistar.patients import routes_patients
from mapistar.permissions import ActesPermissionsComponent, IsAuthenticated
from mapistar.theso import routes_theso
from mapistar.users import routes_users
from mapistar.utils import check_config

check_config(settings)

routes = [
    routes_patients,
    routes_observations,
    routes_ordonnances,
    routes_medicaments,
    routes_theso,
    routes_users,
]
components = [JWT(settings.JWT), ActesPermissionsComponent()]


app = App(
    routes=routes,
    components=components,
    event_hooks=[PonyDBSession(), IsAuthenticated()],
    schema_url="/schemas/",
)
"""
curl -H "Content-Type: application/json" -X POST -d '{"nom":"xyz","prenom":"xyz", "ddn":"1234-12-12"}'
http://localhost:8080/create/
"""
