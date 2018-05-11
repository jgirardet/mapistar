# Third Party Libraries
from apistar import App
from apistar_jwt.token import JWT
from apistar_ponyorm import PonyDBSession
from simple_settings import settings

# mapistar
# from mapistar.actes.views import routes_medicaments, routes_ordonnances
from mapistar.actes.routes import (
    routes_observations,
    routes_ordonnances,
    routes_medicaments,
)
from mapistar.patients import routes_patients
from mapistar.permissions import ActesPermissionsComponent, IsAuthenticated
from mapistar.theso import routes_theso
from mapistar.users import routes_users

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
    # event_hooks=[PonyDBSession()],
    schema_url="/schema/",
)
"""
curl -H "Content-Type: application/json" -X POST -d '{"nom":"xyz","prenom":"xyz", "ddn":"1234-12-12"}'
http://localhost:8080/create/
"""

if __name__ == "__main__":
    # app.serve(ho starun_wsgi(app)
    options = {"use_debugger": True, "use_reloader": True}
    app.serve("127.0.0.1", 5000, **options)
