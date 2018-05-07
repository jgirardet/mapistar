# Third Party Libraries
# Standard Libraries
# Standard Libraries
# Standard Libraries
# Standard Libraries
# Standard Libraries
from pathlib import Path  # python3 only

import pendulum
from dotenv import load_dotenv

# modules where to import pony  models
models = ["patients", "users", "actes", "ordonnances"]

TZ = pendulum.timezone("Europe/Paris")


env_path = Path(".").parent / ".env"
load_dotenv(env_path)
