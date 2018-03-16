#!/usr/bin/env python
from config import settings
from importlib import import_module
# from mapistar.pony_backend import db

import sys
from pathlib import Path

pony_config = settings.PONY
entities_filename = pony_config.get('entities_filename', "models")
db_params = pony_config['DATABASE']
project = pony_config['PROJECT_NAME']

print(sys.argv)
# models = []
if sys.argv[1] == 'make':
    app = sys.argv[2]
    entity = sys.argv[3]
    model = import_module('.'.join((project, app, entities_filename)))
    migration_dir = Path(project) / app / model.__file__ / "migrations"
    migration_dir.
    entity = getattr(model, sys.argv[3])
    model.db.migrate(
        command='make', migration_dir=str(migration_dir), **db_params)

# for app in pony_config['INSTALLED_APPS']:
#     model = import_module('.'.join((project, app, entities_filename)))
