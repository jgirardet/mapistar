# Third Party Libraries
import pytest
from users.utils import get_payload


def test_get_payload_user(user):
    pl = get_payload(user, {'seconds': 3})
    assert pl['user_id'] == user.id


def test_get_payload_duration_empty():
    with pytest.raises(ValueError):
        pl = get_payload(user='jlj', duration={})
