# Standard Libraries
from datetime import datetime
from unittest.mock import MagicMock

# Third Party Libraries
import pendulum
import pytest
from apistar import exceptions

# mapistar
from mapistar.permissions import ActesPermissionsComponent

pytestmark = pytest.mark.pony


@pytest.fixture(scope="function")
def actes_permission(request, observation):
    m = MagicMock()
    m.user.id = 999
    p = ActesPermissionsComponent()
    p.user = m
    p.obj = observation
    return p


class TestActesPermission:

    def test_aonly_owner_can_edit(self, actes_permission):

        with pytest.raises(exceptions.Forbidden) as e:
            actes_permission.only_owner_can_edit()
        assert (
            str(e.value)
            == "Un utilisateur ne peut modifier un acte créé par un autre utilisateur"
        )

    def test_only_editable_today(self, actes_permission):
        a = actes_permission
        a.obj.created = pendulum.yesterday()
        with pytest.raises(exceptions.BadRequest) as e:
            a.only_editable_today()
        assert str(e.value) == "Un acte ne peut être modifié en dehors du jours même"

    def test_only_editable_today_23h_utc(self, actes_permission):
        a = actes_permission
        a.obj.created = datetime(2012, 12, 12, 23, 50)
        fakedatetime = pendulum.datetime(
            2012, 12, 13, 0, 30, tz=pendulum.timezone("Europe/Paris")
        )
        with pendulum.test(fakedatetime):
            assert a.only_editable_today() == None
