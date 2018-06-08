from typing import TypeVar

from apistar import Component
from apistar_jwt import JWTUser

from mapistar.users import User
from mapistar.utils import get_or_404

UserC = TypeVar("UserC")


class UserComponent(Component):
    def resolve(self, user: JWTUser) -> UserC:
        return get_or_404(User, user.id)
