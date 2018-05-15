# Standard Libraries
import json
from unittest.mock import MagicMock, Mock

# Third Party Libraries
import pytest
from mapistar.actes.ordo_items import Item, ItemViews, Medicament
from mapistar.utils import DicoMixin, SetMixin, NameMixin


jwtuser = Mock(**{"id": 15})

inst = MagicMock(**{"dico": {"le": "dico"}})

litem = MagicMock(spec=Item, return_value=inst)


class ItemTest(ItemViews):
    model = litem
    schema_add = dict()
    schema_update = dict()


class TestItemViews:

    def test_add_item(self, mocker, mordo):
        r = ItemTest.add_item()(
            data={"cip": "1234567890123", "nom": "Un Médoc"}, obj=mordo
        )
        assert json.loads(r.content) == {"le": "dico"}
        assert r.status_code == 201
        litem.assert_called_with(ordonnance=mordo, cip="1234567890123", nom="Un Médoc")

    def test_delete_item(self, mocker, mitem):
        r = ItemTest.delete_item()(99, mitem)

        mitem.delete.assert_called_once()
        assert r == {"id": 99, "deleted": True}

    def test_update_item(self, mocker, mitem):
        upd = {"modified": "123456"}
        t = ItemTest.update_item()(47, upd, mitem)

        mitem.set.assert_called_with(modified="123456")
        assert t == mitem.dico


class TestItemModel:

    def test_inheritance(self):
        assert issubclass(Item, DicoMixin)
        assert issubclass(Item, SetMixin)
        assert issubclass(Item, NameMixin)

    def test_after_insert(self, mitem, mordo, mocker):
        mitem.ordonnance = mordo
        mordo.created = "lalala"
        Item.after_insert(mitem)

        mordo.before_update.assert_called()
        mordo.ordre_add_item.assert_called_with(mitem)

    def test_after_delete(self, mitem, mordo):
        mitem.ordonnance = mordo
        Item.before_delete(mitem)

        mordo.before_update.assert_called()
        mordo.ordre_delete_item.assert_called_with(mitem)

    def test_after_udpate(self, mitem, mordo):
        # mocker.patch("datettime")
        mitem.ordonnance = mordo

        Item.before_update(mitem)

        mordo.before_update.assert_called()

    @pytest.mark.pony
    def test_item_update_ordonnnace(self, ordonnance, ponydb):
        debut = ordonnance.modified
        i = ponydb.Item(ordonnance=ordonnance)
        i.flush()
        after_insert = ordonnance.modified
        i.place = 2
        i.flush()
        after_modif = ordonnance.modified
        i.delete()
        ordonnance.flush()
        after_delete = ordonnance.modified
        assert debut < after_insert < after_modif < after_delete


class TestMedicamentModel:

    def test_repr(self, mitem):
        mitem.nom = "Bla bla"
        assert Medicament.__repr__(mitem) == "[Medicament: Bla bla]"
