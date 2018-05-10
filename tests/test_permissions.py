# Standard Libraries
from datetime import datetime
from unittest.mock import MagicMock

# Third Party Libraries
import pendulum
import pytest
from apistar import exceptions

# mapistar
from mapistar.permissions import ActesPermissionsComponent, ActesPermissions

pytestmark = pytest.mark.pony

from mapistar.exceptions import MapistarProgrammingError
from tests.factory import itemf


@pytest.fixture(scope="function")
def actes_permission_comp(request, observation):
    m = MagicMock()
    m.user.id = 999
    p = ActesPermissionsComponent()
    p.user = m
    p.obj = observation
    return p


@pytest.fixture(scope="function")
def actes_permissions(request, observation, user):
    ap = ActesPermissions(observation, user)
    return ap


class TestActesPermission:

    def test_only_owner_can_edit(self, actes_permissions):

        with pytest.raises(exceptions.Forbidden) as e:
            actes_permissions.only_owner_can_edit()
        assert (
            str(e.value)
            == "Un utilisateur ne peut modifier un acte créé par un autre utilisateur"
        )

    def test_only_editable_today(self, actes_permissions):
        actes_permissions.acte.created = pendulum.yesterday()
        with pytest.raises(exceptions.BadRequest) as e:
            actes_permissions.only_editable_today()
        assert str(e.value) == "Un acte ne peut être modifié en dehors du jours même"

    def test_only_editable_today_23h_utc(self, actes_permissions):
        actes_permissions.acte.created = datetime(2012, 12, 12, 23, 50)
        fakedatetime = pendulum.datetime(
            2012, 12, 13, 0, 30, tz=pendulum.timezone("Europe/Paris")
        )
        with pendulum.test(fakedatetime):
            assert not actes_permissions.only_editable_today()


class TestActesPermissionComponent:

    @pytest.mark.parametrize("genre", ["acte_id", "item_id"])
    def test_ActesPermissions_called(self, mocker, actes_permission_comp, genre):
        mocker.patch("mapistar.permissions.get_or_404")
        ap = mocker.patch("mapistar.permissions.ActesPermissions")
        print(genre)
        actes_permission_comp.resolve(params={genre: 1}, user=1)
        assert ap.is_called_once()

    def test_returns_actes_with_acte_id(
        self, observation, mocker, actes_permission_comp
    ):
        mocker.patch("mapistar.permissions.ActesPermissions")
        obj = actes_permission_comp.resolve(params={"acte_id": observation.id}, user=1)
        assert observation is obj

    def test_returns_item_with_item_id(self, item, mocker, actes_permission_comp):
        mocker.patch("mapistar.permissions.ActesPermissions")
        obj = actes_permission_comp.resolve(params={"item_id": item.id}, user=1)
        assert item is obj

    def test_resolve_exclude_acteid_and_itemid(self, actes_permission_comp):
        with pytest.raises(MapistarProgrammingError) as exc:
            actes_permission_comp.resolve(params={"acte_id": 1, "item_id": 1}, user=1)
        assert (
            str(exc.value)
            == "Une requête ne peut spécifier item_id et acte_id à la fois"
        )
