from typing import TypeVar

from apistar import Component
from apistar_jwt import JWTUser

from mapistar.base_db import db
from mapistar.utils import get_or_404

UserC = TypeVar("UserC")
