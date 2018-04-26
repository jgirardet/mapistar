# Standard Libraries
import os
from urllib.parse import urlparse

from .base import *

print("Testing Config")

JWT = {"JWT_SECRET": "a"}


# sqlite memory
DATABASE = {"provider": "sqlite", "filename": ":memory:", "create_tables": True}

# sqlite file_db
# DATABASE = {
#     "provider": "sqlite",
#     "filename": "db.sqlite",
#     "create_tables": True,
#     "create_db": True,
# }

# url = urlparse(os.environ["MAPISTAR_DATABASE"])
# DATABASE = {
#     "provider": url.scheme,
#     "host": url.hostname,
#     "port": url.port,
#     "database": "mapistar_test",
#     "user": url.username,
#     "password": url.password,
#     "create_tables": True,
# }
