# mapistar
from mapistar.models import db

from .views import ActesViews

# routes_actes = Include(
#     url='/actes',
#     name='actes',
#     routes=[
#         Route(url="/", method="POST", handler=add),
#         # Route(url="/", method="GET", handler=liste),
#         # Route(url="/{pk}/", method="PUT", handler=update),
#         # # Route(url="/patients/", method="DELETE", handler=delete),
#         # Route(url="/{pk}/", method="DELETE", handler=delete),
#         # Route(url="/{pk}/", method="GET", handler=get),
#     ])
# #

VObs = ActesViews(db.Observation)
routes_actes = VObs.urls()
