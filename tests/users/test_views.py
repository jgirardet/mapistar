# Standard Libraries
import json

# Third Party Libraries
import pytest
from apistar import reverse_url
from app import settings

from users.models import User

pytestmark = pytest.mark.django_db


def test_login_pass(client_anonymous):
    User.objects.create_user(username='hh', password='hh')
    response = client_anonymous.post(
        reverse_url('login', user="hh", pwd="hh", settings=settings))
    assert response.status_code == 201


def test_login_forbiden_bad_user(client_anonymous):
    response = client_anonymous.post(
        reverse_url(
            'login', user="fzefzefzefzef", pwd="fzefzefzef",
            settings=settings))
    assert response.status_code == 403


def test_login_forbiden_inactive_user(client_anonymous):
    User.objects.create_user(username='hh', password='hh', is_active=False)
    response = client_anonymous.post(
        reverse_url('login', user="hh", pwd="hh", settings=settings))
    assert response.status_code == 403
