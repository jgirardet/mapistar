# Standard Libraries
from pathlib import Path  # python3 only

# Third Party Libraries
import pendulum
from dotenv import load_dotenv

# modules where to import pony  models

actes_models = ("actes", ("observations", "ordonnances", "ordo_items"))

# models = ("patients", "users", actes_models)
models = ("patients", "users", "actes.observations", "actes.ordonnances")

TZ = pendulum.timezone("Europe/Paris")


env_path = Path(".").parent / ".env"
load_dotenv(env_path)
