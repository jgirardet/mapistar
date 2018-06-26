# Standard Libraries
from datetime import datetime, timedelta

# Third Party Libraries
import pendulum
import pytest
from apistar import exceptions

# mapistar
from mapistar.exceptions import MapistarProgrammingError
from mapistar.permissions import ActesPermissions, ActesPermissionsComponent
from mapistar.documents import Document
from mapistar.actes.actes import Acte
from mapistar.actes.ordo_items import Item
from unittest.mock import patch


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
        assert not r

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


# @pytest.mark.pony(reset_db=False)
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

    def test_returns_document_with_document_id(self, mocker):
        mocker.patch("mapistar.permissions.ActesPermissions")
        document = mocker.Mock()
        mocker.patch("mapistar.permissions.get_or_404", return_value=document)
        obj = AP.resolve(params={"document_id": 1}, user=1)

        assert document is obj

    def test_get_404_call(self, mocker):
        m = mocker.patch("mapistar.permissions.ActesPermissions")
        q = mocker.patch("mapistar.permissions.get_or_404")
        a = AP.resolve(params={"acte_id": 1}, user=1)
        b = AP.resolve(params={"item_id": 1}, user=1)
        c = AP.resolve(params={"document_id": 1}, user=1)
        c = mocker.call
        q.assert_has_calls([c(Acte, 1), c(Item, 1), c(Document, 1)])
        m.assert_has_calls(
            [
                c(q.return_value, 1),
                c()(),
                c(q.return_value.ordonnance, 1),
                c()(),
                c(q.return_value.acte, 1),
                c()(),
            ]
        )

    def test_resolve_exclude_acteid_and_itemid(self):
        with pytest.raises(MapistarProgrammingError) as exc:
            AP.resolve(params={"acte_id": 1, "item_id": 1}, user=1)
        assert (
            str(exc.value)
            == "Une requête ne peut spécifier seulement acte_id ou item_id ou document_id"
        )
