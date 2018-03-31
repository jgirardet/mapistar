from pythonthesorimed.thesoitem import ThesoItem
from apistar import Include, Route

theso_session = ThesoItem('localhost', 'thesorimed', 'j', 'j')

from .utils import MapistarValidator


def fuzzy(chaine: str):
    return theso_session.fuzzy(chaine)


routes_theso = Include(
    url='/theso',
    name='theso',
    routes=[
        Route(url="/fuzzy/{chaine}/", method="GET", handler=fuzzy),
    ])