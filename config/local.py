# Standard Libraries
import os
from urllib.parse import urlparse

from .base import *

print("Local Config")

JWT = {"JWT_SECRET": "a"}


# forme : postgres://user:password@host:port/databasename
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

# sqlite memory
DATABASE = {"provider": "sqlite", "filename": ":memory:", "create_tables": True}
