# Third Party Libraries
from django.utils import timezone

from .models import User


def get_payload(user: User, duration: dict) -> dict:
    """
    Returns a payload based on User
    duration is a dict to pass to timedelta
    """
    if not duration:
        raise ValueError('duration  cannot be empty')
    return {
        'user_id': user.id,
        'iat': timezone.now(),
        'exp':
            timezone.now() + timezone.timedelta(**duration)  # ends in 10 minutes
    }
