from apistar import App
from apistar_jwt.token import JWT
from apistar_ponyorm import PonyDBSession
from simple_settings import settings

from mapistar import db  # noqa: F401   do not remove, does mapping
from mapistar.actes.routes import (
    routes_divers,
    routes_medicaments,
    routes_observations,
    routes_ordonnances,
)

# from mapistar.patients import routes_patients
# from mapistar.permissions import ActesPermissionsComponent, IsAuthenticated
# from mapistar.theso import routes_theso
# from mapistar.users import UserComponent, routes_users
# from mapistar.documents import routes_documents
# from mapistar.utils import check_config


check_config(settings)

routes = [
    routes_patients,
    routes_observations,
    routes_ordonnances,
    routes_medicaments,
    routes_theso,
    routes_users,
    routes_divers,
    routes_documents,
]
components = [JWT(settings.JWT), ActesPermissionsComponent(), UserComponent()]

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
