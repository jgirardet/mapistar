""" 
    Apistar Main App
"""

# Third Party Libraries
from apistar.frameworks.wsgi import WSGIApp as App
from apistar_shell import commands as apistar_shell_commands
from apistar_shell import components as apistar_shell_components
from pony.orm import Database
from config import settings
from config.urls import routes
from mapistar.pony_backend import components as pony_components
# from mapistar.pony_backend import commands as pony_commands
# from mapistar.pony_backend import db
# collect All components
components = [
    *apistar_shell_components.components,
    *pony_components,
]

commands = [*apistar_shell_commands.common_commands, ]


app = App(
    routes=routes,
    components=components,
    commands=commands,
    settings=settings.__dict__)

# app = App(
#     routes=routes, settings=settings, commands=commands, components=components)

if __name__ == '__main__':
    app.main()
