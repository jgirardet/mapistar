# Third Party Libraries
from pytz import timezone

JWT = {"JWT_SECRET": "a"}


# modules where to import models
models = ["patients", "users", "actes", "ordonnances"]

tz = timezone("Europe/Paris")
