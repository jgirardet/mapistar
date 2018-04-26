# Third Party Libraries
from simple_settings import settings

# mapistar
from mapistar.base_db import db
from mapistar.utils import import_models

import_models(settings.models)


db.connect(**settings.DATABASE)
