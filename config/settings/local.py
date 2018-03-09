# Third Party Libraries
from apistar.backends.django_orm import Session as DB
from apistar.interfaces import Auth

# mapistar
from mapistar.users.authentication import AuthUser

from .base import *

# PERMISSIONS.clear()
# AUTHENTICATION.clear()


JWT['PAYLOAD_DURATION'] = {'seconds': 9000}


# change authentication for local use
class LocalAuthentification():
    def authenticate(self, db: DB):
        user = db.User.objects.get(username='j')
        print(user)
        return AuthUser(user=user)


AUTHENTICATION.insert(0, LocalAuthentification())
