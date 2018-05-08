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

from mapistar.exceptions import MapistarProgrammingError
from tests.factory import itemf


@pytest.fixture(scope="function")
def actes_permission(request, observation):
    m = MagicMock()
    m.user.id = 999
    p = ActesPermissionsComponent()
    p.user = m
    p.obj = observation
    return p


class TestActesPermission:

    def test_run_actes_permissions_with_acte_id(self, mocker, actes_permission):
        mocker.patch("mapistar.permissions.get_or_404")
        mocker.patch.object(actes_permission, "run_actes_permissions")
        actes_permission.resolve(params={"acte_id": 1}, jwt_user=1)
        actes_permission.run_actes_permissions.assert_called_once()

    def test_permissions_called_with_item_id(self, mocker, actes_permission):
        mocker.patch("mapistar.permissions.get_or_404")
        mocker.patch.object(actes_permission, "run_actes_permissions")
        actes_permission.resolve(params={"acte_id": 1}, jwt_user=1)
        assert actes_permission.run_actes_permissions.is_called_once()

    def test_returns_actes_with_acte_id(self, observation, mocker, actes_permission):
        mocker.patch.object(actes_permission, "run_actes_permissions")
        obj = actes_permission.resolve(params={"acte_id": observation.id}, jwt_user=1)
        assert observation is obj

    def test_returns_item_with_item_id(self, ordonnance, mocker, actes_permission):
        item = itemf(ordonnance=ordonnance)
        item.flush()
        mocker.patch.object(actes_permission, "run_actes_permissions")
        obj = actes_permission.resolve(params={"item_id": item.id}, jwt_user=1)
        assert item is obj

    def test_resolve_exclude_acteid_and_itemid(self, actes_permission):
        with pytest.raises(MapistarProgrammingError) as exc:
            actes_permission.resolve(params={"acte_id": 1, "item_id": 1}, jwt_user=1)
        assert (
            str(exc.value)
            == "Une requête ne peut spécifier item_id et acte_id à la fois"
        )

    def test_only_owner_can_edit(self, actes_permission):

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
            assert not a.only_editable_today()
