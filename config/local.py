# Standard Libraries
import os  # noqa: F401
# forme : postgres://user:password@host:port/databasename
from urllib.parse import urlparse

from .base import *  # noqa: F401,F403

print("Local Config")

JWT = {"JWT_SECRET": "a"}


url = urlparse(os.environ["MAPISTAR_DATABASE"])
DATABASE = {
    "provider": url.scheme,
    "host": url.hostname,
    "port": url.port,
    "database": "mapistar_test",
    "user": url.username,
    "password": url.password,
    "create_tables": True,
}

# sqlite memory
# DATABASE = {"provider": "sqlite", "filename": ":memory:", "create_tables": True}
