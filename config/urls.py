# Third Party Libraries
from actes.urls import actes_urls
from apistar import Include
from apistar.handlers import docs_urls, static_urls
from config.settings import ACTES_URL
from patients.urls import patients_urls
from users.urls import users_urls

routes = [
    Include('/docs', docs_urls),
    Include('/static', static_urls),
    Include('/patients', patients_urls),
    Include('/users', users_urls),
    Include(ACTES_URL, actes_urls),
]
