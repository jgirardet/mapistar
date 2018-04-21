# Standard Libraries
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
