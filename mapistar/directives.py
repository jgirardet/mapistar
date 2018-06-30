
from mapistar.auth import JsonWebToken
from simple_settings import settings
import hug


JBB = JsonWebToken(settings.JWT)


@hug.directive(apply_globally=True)
def jwt(default=None, **kwargs):
    return JBB
