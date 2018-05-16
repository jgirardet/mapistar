# Standard Libraries
import json
from unittest.mock import MagicMock, call

# Third Party Libraries
import pytest

# mapistar
from mapistar.actes.ordonnances import (
    Ordonnance, OrdonnanceCreateSchema, OrdonnanceUpdateSchema
)
from mapistar.patients import Patient

# pytestmark = pytest.mark.pony


patientm = MagicMock(spec=Patient, **{"id": 1})


class TestOrdonnanceModel:

    @pytest.mark.pony
    def test_dico(self, ordonnance, ponydb):
        e = ponydb.Item(ordonnance=ordonnance)
        # a.flush()
        dico = ordonnance.dico
        it = dico.pop("items")
        assert it == [e.dico], "confirme le custome d'item"
        assert "created" in dico, "confirme l'appel de super()"

    def test_ordre_add(self, mordo):
        # not ordre
        mordo.ordre = ""
        Ordonnance.ordre_add_item(mordo, MagicMock(**{"id": 22}))
        assert mordo.ordre == "22"
        # ordre >0
        Ordonnance.ordre_add_item(mordo, MagicMock(**{"id": 44}))
        assert mordo.ordre == "22-44"

    def test_ordre_delete(self, mordo):
        # many
        mordo.ordre = "12-26-44-54"
        Ordonnance.ordre_delete_item(mordo, MagicMock(**{"id": 26}))
        assert mordo.ordre == "12-44-54"
        Ordonnance.ordre_delete_item(mordo, MagicMock(**{"id": 12}))
        assert mordo.ordre == "44-54"
        Ordonnance.ordre_delete_item(mordo, MagicMock(**{"id": 54}))
        assert mordo.ordre == "44"
        # one
        Ordonnance.ordre_delete_item(mordo, MagicMock(**{"id": 44}))
        assert mordo.ordre == ""

    def test_get_ordered_items(self, mocker, mordo):
        # no item
        mordo.ordre = ""
        a = Ordonnance.get_ordered_items(mordo)
        assert a == []
        # normal
        mordo.ordre = "45-25-32"
        x, y, z = [mocker.Mock(**{"id": x}, name=str(x)) for x in [25, 32, 45]]
        mordo.items = [x, y, z]
        a = Ordonnance.get_ordered_items(mordo)

        assert a == [z, x, y]

        # valueerro
        mordo.ordre = "1-22-4"
        mordo.items = MagicMock()
        mordo.items.select.return_value = [x, y, z]
        mocker.patch("builtins.sorted", side_effect=ValueError)
        a = Ordonnance.get_ordered_items(mordo)
        mocker.stopall()

        mordo.ordre_add_item.call_args_list == [call(x), call(y), call(z)]
        assert a == []  # only check return list

        # valueerro
        mordo.ordre = "1-22-4"
        mordo.items = MagicMock()
        l = mocker.patch("builtins.list")
        a = Ordonnance.get_ordered_items(mordo)
        mocker.stopall()

        l.assert_called_with(mordo.items)
