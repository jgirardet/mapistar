# Standard Libraries
import os  # noqa: F401

from .base import *  # noqa: F401,F403

print("Testing Config")

JWT = {"JWT_SECRET": "a"}

JWT_DURATION = 10

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
