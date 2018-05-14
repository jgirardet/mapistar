# Third Party Libraries
from simple_settings import settings

# mapistar
from mapistar.base_db import db
from mapistar.utils import import_models

import_models(settings.MODELS)


# db.connect(**settings.DATABASE)

settings.DATABASE.pop("create_tables")

# db.bind(provider="sqlite", filename=":memory:")


db.bind(**settings.DATABASE)

db.generate_mapping(create_tables=True)
