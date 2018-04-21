#!/usr/bin/env python

# Standard Libraries
# get database conf
import os
from urllib.parse import urlparse

# mapistar
from mapistar import settings
# from mapistar.base_db import db
from mapistar.base_db import db
from mapistar.utils import import_models

# import Entities
import_models(settings.models)


url = urlparse(os.environ["MAPISTAR_PONY_DB"])


db_params = dict(
    provider=url.scheme,
    host=url.hostname,
    database=url.path.strip("/"),
    user=url.username,
    password=url.password,
    port=url.port,
)


db.migrate(**db_params, migration_dir="mapistar/migrations")
