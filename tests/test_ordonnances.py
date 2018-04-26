# Third Party Libraries
import pytest
from tests.factory import itemf

pytestmark = pytest.mark.pony


class TestOrdonnanceModel:

    def test_dico_super_is_called(self, ordonnance, ponydb):
        for i in range(3):
            a = ponydb.Item(ordonnance=ordonnance)
        dico = ordonnance.dico
        dico.pop("items")
        assert isinstance(dico["created"], str), "confirme l'appel de super()"

    def test_item_in_dico_ordre_ok(self, ordonnance, ponydb):
        i = itemf(ordonnance=ordonnance)
        j = itemf(ordonnance=ordonnance)
        k = itemf(ordonnance=ordonnance)
        ponydb.flush()
        ordonnance.ordre = f"-{j.id}-{k.id}-{i.id}"
        d = ordonnance.dico["items"]
        assert [x["id"] for x in d] == [j.id, k.id, i.id]


# assert str(
#     items
# ) == "['id': 1, 'ordonnance': 1, 'place': 1, 'classtype': 'Item'}, {'id': 2, 'ordonnance': 1, 'place': 2, 'classtype': 'Item'}, {'id': 3, 'ordonnance': 1, 'place': 3, 'classtype': 'Item'}]"


class TestItemModel:

    def test_update_modified(self, ordonnance, ponydb):
        debut = ordonnance.modified
        i = ponydb.Medicament(ordonnance=ordonnance, cip="km", nom="omokm")
        i.flush()
        after_insert = ordonnance.modified
        i.duree = 3
        i.flush()
        after_modif = ordonnance.modified
        i.delete()
        ordonnance.flush()
        after_delete = ordonnance.modified
        assert debut < after_insert < after_modif < after_delete

    def test_update_ordre_at_insert(self, ordonnance):
        i = itemf(ordonnance=ordonnance)
        j = itemf(ordonnance=ordonnance)
        assert ordonnance.dico["ordre"] == f"-{i.id}-{j.id}"

    def test_update_ordre_at_delete(self, ordonnance):
        i = itemf(ordonnance=ordonnance)
        j = itemf(ordonnance=ordonnance)
        k = itemf(ordonnance=ordonnance)
        ordonnance.dico
        j.delete()
        assert ordonnance.dico["ordre"] == f"-{i.id}-{k.id}"
