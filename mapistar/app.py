# Third Party Libraries
from apistar import App
from apistar_jwt.token import JWT
from apistar_ponyorm import PonyDBSession

# mapistar
from mapistar import settings
from mapistar.actes.urls import routes_actes
from mapistar.patients import routes_patients
from mapistar.theso import routes_theso
from mapistar.users import routes_users
from mapistar.permissions import ActesPermissionsComponent, IsAuthenticated

components = [JWT(settings.JWT), ActesPermissionsComponent()]

app = App(
    routes=[routes_patients, routes_actes, routes_theso, routes_users],
    components=components,
    event_hooks=[PonyDBSession(), IsAuthenticated()],
    schema_url="/schema/",
)
"""
curl -H "Content-Type: application/json" -X POST -d '{"nom":"xyz","prenom":"xyz", "ddn":"1234-12-12"}' http://localhost:8080/create/
"""

if __name__ == "__main__":
    # app.serve(ho starun_wsgi(app)
    options = {"use_debugger": True, "use_reloader": True}
    app.serve("127.0.0.1", 5000, **options)
