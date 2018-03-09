# Third Party Libraries
import pytest
from actes.actesviews import ActesViews
from actes.models import Observation
from actes.permissions import ActesWritePermission
from apistar.exceptions import BadRequest, Forbidden
from django.utils import timezone
from tests.factories import FacUser

pytestmark = pytest.mark.django_db

awp = ActesWritePermission(ActesViews(Observation))


def test_pass(auth_user, observation):
    obs = observation(owner=auth_user.user)
    assert awp.has_permission(obj_id=obs.id, auth=auth_user)


def test_reject_not_owner(auth_user, observation):
    obs = observation(owner=FacUser())
    with pytest.raises(Forbidden):
        awp.has_permission(obj_id=obs.id, auth=auth_user)


def test_only_today(observation, auth_user):
    obs = observation(owner=auth_user.user)
    obs.created += timezone.timedelta(days=-1)
    obs.save()
    with pytest.raises(BadRequest):
        awp.has_permission(obs.id, auth_user)
