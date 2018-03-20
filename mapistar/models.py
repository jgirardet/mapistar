from pony import orm

from mapistar.base_db import db
from mapistar.patients.models import *

from config.settings import PONY
db.bind(**PONY['DATABASE'])
db.generate_mapping(create_tables=True)