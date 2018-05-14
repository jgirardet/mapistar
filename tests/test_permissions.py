from mapistar.permissions import ActesPermissions, ActesPermissionsComponent

import pytest
from apistar import exceptions
import pendulum
from datetime import datetime, timedelta
from mapistar.exceptions import MapistarProgrammingError
import json


class TestActesPermission:

    def test_only_owner_can_edit2(self, mocker):

        a = ActesPermissions(mocker.Mock(**{"owner.id": 1}), mocker.Mock(**{"id": 2}))
        print(a.acte.owner.id, a.user.id)

        with pytest.raises(exceptions.Forbidden) as e:
            a.only_owner_can_edit()
        assert (
            str(e.value)
            == "Un utilisateur ne peut modifier un acte créé par un autre utilisateur"
        )
        # should pass
        a.acte.owner.id = 2
        print(a.acte.owner.id, a.user.id)
        r = a.only_owner_can_edit()
        assert r == None

    def test_only_editable_today(self, mocker):
        b = datetime.utcnow() - timedelta(days=1)
        a = ActesPermissions(mocker.Mock(**{"created": b}), 1)
        with pytest.raises(exceptions.BadRequest) as e:
            a.only_editable_today()
        assert str(e.value) == "Un acte ne peut être modifié en dehors du jours même"

    def test_only_editable_today_23h_utc(self, mocker):
        a = ActesPermissions(
            mocker.Mock(**{"created": datetime(2012, 12, 12, 23, 50)}), 1
        )
        fakedatetime = pendulum.datetime(
            2012, 12, 13, 0, 30, tz=pendulum.timezone("Europe/Paris")
        )
        with pendulum.test(fakedatetime):
            assert not a.only_editable_today()

    def test_perm_are_called(self, mocker):
        a = mocker.Mock()
        ActesPermissions.__call__(a)
        a.only_owner_can_edit.assert_called_once()
        a.only_editable_today.assert_called_once()


AP = ActesPermissionsComponent()


class TestActesPermissionComponent:

    @pytest.mark.parametrize("genre", ["acte_id", "item_id"])
    def test_ActesPermissions_called(self, mocker, genre):
        mocker.patch("mapistar.permissions.get_or_404")
        ap = mocker.patch("mapistar.permissions.ActesPermissions")
        AP.resolve(params={genre: 1}, user=1)

        ap.assert_called_once()

    def test_returns_actes_with_acte_id(self, mocker):
        mocker.patch("mapistar.permissions.ActesPermissions")
        mocker.patch("mapistar.permissions.get_or_404", return_value="acte")
        obj = AP.resolve(params={"acte_id": 1}, user=1)

        assert obj == "acte"

    def test_returns_item_with_item_id(self, mocker):
        mocker.patch("mapistar.permissions.ActesPermissions")
        item = mocker.Mock()
        mocker.patch("mapistar.permissions.get_or_404", return_value=item)
        obj = AP.resolve(params={"item_id": 1}, user=1)

        assert item is obj

    def test_resolve_exclude_acteid_and_itemid(self):
        with pytest.raises(MapistarProgrammingError) as exc:
            AP.resolve(params={"acte_id": 1, "item_id": 1}, user=1)
        assert (
            str(exc.value)
            == "Une requête ne peut spécifier item_id et acte_id à la fois"
        )

    def test_resolve_not_acteid_or_itmeid(self):
        with pytest.raises(MapistarProgrammingError) as exc:
            AP.resolve(params={}, user=1)
        assert str(exc.value) == "doit préciser acte_id ou item_id"
