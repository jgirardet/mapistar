from pony import orm

from mapistar.base_db import db
from .patients import Patient

# from config.settings import PONY
# db.bind(**PONY['DATABASE'])
db.connect(
    provider="sqlite",
    filename="db.sqlite3",
    create_tables=True,
    create_db=True,
    # allow_auto_upgrade=True,
)
# db.generate_mapping(create_tables=True)