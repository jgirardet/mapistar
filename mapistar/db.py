# Standard Libraries
from urllib.parse import urlparse

# mapistar
from mapistar import settings
from mapistar.base_db import db
from mapistar.utils import import_models

import_models(settings.models)

# db.connect(provider="sqlite", filename="db.sqlite", create_tables=True, create_db=True)

# try:
#     os.environ['TEST_RUNNING']
# except KeyError:
# url = urlparse(os.environ['MAPISTAR_PONY_DB'])
url = urlparse("postgres://j:j@localhost:5432/mapistar")
# db.connect(
#     provider=url.scheme,
#     host=url.hostname,
#     database=url.path.strip("/"),
#     user=url.username,
#     password=url.password,
#     port=url.port,
#     create_tables=True,
# )

# else:
db.connect(provider="sqlite", filename=":memory:", create_tables=True)
# create_db=True,
# )
