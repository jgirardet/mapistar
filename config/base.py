import pendulum


# modules where to import pony  models
models = ["patients", "users", "actes", "ordonnances"]

TZ = pendulum.timezone("Europe/Paris")
