# Third Party Libraries
from pony import orm

# mapistar
from mapistar.base_db import db

from .patients import Patient
from .users import User
from mapistar.actes.models import Acte, Observation
# from config.settings import PONY
# db.bind(**PONY['DATABASE'])
import os
from urllib.parse import urlparse

try:
    os.environ['TEST_RUNNING']
except KeyError:
    url = urlparse(os.environ['MAPISTAR_PONY_DB'])
    db.connect(
        provider=url.scheme,
        host=url.hostname,
        database=url.path.strip('/'),
        user=url.username,
        password=url.password,
        port=url.port,
        create_tables=True,
    )
else:
    db.connect(
        provider="sqlite",
        filename=":memory:",
        create_tables=True,
    )
