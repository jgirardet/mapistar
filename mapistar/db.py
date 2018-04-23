# mapistar
from mapistar.base_db import db
from mapistar.utils import import_models

from simple_settings import settings

import_models(settings.models)


db.connect(**settings.DATABASE)
