# Standard Libraries
import os  # noqa: F401

# from urllib.parse import urlparse

from .base import *  # noqa: F401,F403

print("Local Config")

JWT = {"secret": "a", "white_list": ["/", "/users/login"]}

JWT_DURATION = 3600

# forme : postgres://user:password@host:port/databasename

# url = urlparse(os.environ["MAPISTAR_DATABASE"])
# DATABASE = {
#     "provider": url.scheme,
#     "host": url.hostname,
#     "port": url.port,
#     "database": url.path.strip("/"),
#     "user": url.username,
#     "password": url.password,
#     "create_tables": True,
# }

# sqlite memory
DATABASE = {"provider": "sqlite", "filename": ":memory:", "create_tables": True}
#
