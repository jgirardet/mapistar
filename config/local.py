from .base import *

print("Local Config")

JWT = {"JWT_SECRET": "a"}

# db.connect(provider="sqlite", filename="db.sqlite", create_tables=True, create_db=True)

# try:
#     os.environ['TEST_RUNNING']
# except KeyError:
url = urlparse(os.environ["MAPISTAR_DATABASE"])
# forme : postgres://user:password@host:port/databasename
# url = urlparse("postgres://j:j@localhost:5432/mapistar")
provider = url.scheme,
host = url.hostname,
database = url.path.strip("/"),
user = url.username,
password = url.password,
port = url.port,
create_tables = True,

# else:


# sqlite memory
DATABASE = {"provider": "sqlite", "filename": ":memory:", "create_tables": True}


# create_db=True,
# )
