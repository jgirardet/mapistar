#!/usr/bin/env python

# from mapistar.base_db import db
from mapistar.models import db

import os
from urllib.parse import urlparse

url = urlparse(os.environ['MAPISTAR_PONY_DB'])

db_params = dict(
    provider=url.scheme,
    host=url.hostname,
    database=url.path.strip('/'),
    user=url.username,
    password=url.password,
    port=url.port)

db.migrate(**db_params, migration_dir='mapistar/migrations')