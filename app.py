""" 
    Apistar Main App
"""

# Third Party Libraries
import werkzeug
from apistar import App
from apistar_cerberus import CerberusComp
from apistar_ponyorm import PonyDBSession
from mapistar.actes import routes_actes
from mapistar.patients import routes_patients
from mapistar.theso import routes_theso

app = App(
    routes=[routes_patients, routes_actes, routes_theso],
    components=[CerberusComp()],
    event_hooks=[PonyDBSession()],
    schema_url="/schema/")
"""
curl -H "Content-Type: application/json" -X POST -d '{"nom":"xyz","prenom":"xyz", "ddn":"1234-12-12"}' http://localhost:8080/create/
"""


def run_wsgi(app: App,
             host: str = '127.0.0.1',
             port: int = 8080,
             debug: bool = True,
             reloader: bool = True) -> None:  # pragma: nocover
    """
    Run the development server.
    Args:
      app: The application instance, which should be a WSGI callable.
      host: The host of the server.
      port: The port of the server.
      debug: Turn the debugger [on|off].
      reloader: Turn the reloader [on|off].
    """

    options = {
        'use_debugger': debug,
        'use_reloader': reloader,
        'extra_files': ['app.py']
    }

    werkzeug.run_simple(host, port, app, **options)


if __name__ == '__main__':
    # app.serve(hostarun_wsgi(app)
    options = {
        'use_debugger': True,
        'use_reloader': True,
    }
    app.serve('127.0.0.1', 5000, **options)
