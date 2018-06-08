from .observations import ObservationViews
from .ordo_items import MedicamentViews, DiversViews
from .ordonnances import OrdonnanceViews

routes_observations = ObservationViews.do_routes()
routes_ordonnances = OrdonnanceViews.do_routes()

routes_medicaments = MedicamentViews.routes()
routes_divers = DiversViews.routes()
