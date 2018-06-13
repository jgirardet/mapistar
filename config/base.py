# Standard Libraries
from pathlib import Path  # python3 only

# Third Party Libraries
import pendulum
from dotenv import load_dotenv

# modules where to import pony  models

actes_models = (
    "actes",
    ("observations", "ordonnances", "ordo_items", "correspondances"),
)

# models = ("patients", "users", actes_models)
MODELS = ("patients", "users", actes_models, "theso", "annuaire")

TZ = pendulum.timezone("Europe/Paris")

JWT_DURATION = 0

env_path = Path(".").parent / ".env"
load_dotenv(env_path)
