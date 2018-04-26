# Third Party Libraries
import pytest

pytestmark = pytest.mark.pony


class TestOrdonnanceModel:

    def test_dico(self, ordonnance, ponydb):
        for i in range(3):
            a = ponydb.Item(ordonnance=ordonnance)
        # a.flush()

        dico = ordonnance.dico
        items = dico.pop("items")
        assert isinstance(dico["created"], str), "confirme l'appel de super()"


# assert str(
#     items
# ) == "['id': 1, 'ordonnance': 1, 'place': 1, 'classtype': 'Item'}, {'id': 2, 'ordonnance': 1, 'place': 2, 'classtype': 'Item'}, {'id': 3, 'ordonnance': 1, 'place': 3, 'classtype': 'Item'}]"


class TestItemModel:

    def test_ajout_place(self, ordonnance, ponydb):
        for i in range(3):
            a = ponydb.Item(ordonnance=ordonnance)
        a = ponydb.Item(ordonnance=ordonnance)
        a.flush()
        assert a.place == 4

    def test_update_modified(self, ordonnance, ponydb):
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
