#!/usr/bin/env python
from config import settings
from importlib import import_module
from mapistar.pony_backend import db
from pony.orm import Database
import sys
from pathlib import Path

pony_config = settings.PONY
entities_filename = pony_config.get('entities_filename', "models")
db_params = pony_config['DATABASE']
project = pony_config['PROJECT_NAME']
project_path = Path(__file__)
db_path = project_path.absolute().parent / 'db.local'
print(db_params)

# models = []



command = sys.argv[1]
try:
    command = command + ' ' + sys.argv[2]
except IndexError:
    pass
print(command)
if command == 'make':
    print("helle")
    for app in pony_config['INSTALLED_APPS']:
            model_path='.'.join((project, app, entities_filename))
            import_module(model_path)
db.migrate(command=command, migration_dir="mapistar/migrations", **db_params)
        
