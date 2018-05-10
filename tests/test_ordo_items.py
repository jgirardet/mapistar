# Standard Libraries
import json

# Third Party Libraries
import pytest
from tests.factory import medicamentf, itemf

pytestmark = pytest.mark.pony


class TestMedicamentsViews:

    def test_add(self, ordonnance, cli, app):
        a = {"ordonnance": ordonnance.id, "cip": "1234567890123", "nom": "Un Médoc"}
        r = cli.post(app.reverse_url("medicaments:add_item"), data=json.dumps(a))
        assert r.status_code == 201

    # def test_delete_item(self, ordonnance, cli, app):
    #     print(ordonnance.id)
    #     item = medicamentf(ordonnance=ordonnance)
    #     ordonnance.owner = cli.user
    #     item.flush()
    #     r = cli.delete(app.reverse_url("medicaments:delete_item", item_id=item.id))
    #     assert r.status_code == 200

    def test_delete_item1(self, medicament, cli, app):
        print(medicament.ordonnance.id)

        medicament.ordonnance.owner = cli.user
        r = cli.delete(
            app.reverse_url("medicaments:delete_item", item_id=medicament.id)
        )
        assert r.status_code == 200


# def test_delete_item2(self, item, cli, app):
#     print(item.ordonnance.id)

#     item.ordonnance.owner = cli.user
#     r = cli.delete(app.reverse_url("medicaments:delete_item", item_id=item.id))
#     assert r.status_code == 200


# def test_list_acte_pass(self, ordonnance, app, cli, ponydb):

#     ord = [medicamentf(ordonnance=ordonnance) for i in range(3)]
#     r = cli.get(app.reverse_url("ordonnances:liste", ordonnance_id=ordonnance.id))
#     assert {x["id"] for x in r.json()} == {x.id for x in ord}


# def test_one_pass(self, ordonnance, cli, app):
#     r = cli.get(app.reverse_url("ordonnances:one", acte_id=ordonnance.id))
#     assert r.status_code == 200
#     assert r.json() == ordonnance.dico

# def test_delete_pass(self, ordonnance, cli, app):
#     ordonnance.owner = cli.user
#     r = cli.delete(app.reverse_url("ordonnances:delete", acte_id=ordonnance.id))
#     assert r.status_code == 200
#     with pytest.raises(OperationWithDeletedObjectError):
#         ordonnance.dico

# def test_update_pass(self, cli, app, ordonnance):
#     ordonnance.owner = cli.user
#     upd = {"ordre": "1-2-3-4-5"}
#     r = cli.put(
#         app.reverse_url("ordonnances:update", acte_id=ordonnance.id),
#         data=json.dumps(upd),
#     )
#     assert r.status_code == 200
#     assert r.json()["ordre"] == "1-2-3-4-5"


# def test_add_item(self, ordonnance, cli, app):
#     a = {"ordonnance": ordonnance.id, "cip": "1234567890123", "nom": "Un Médoc"}
#     r = cli.post(
#         app.reverse_url("ordonnances:add_item", ordonnance_id=ordonnance.id),
#         data=json.dumps(a),
#     )
#     print(r.json())
#     assert r.status_code == 201


class TestItemModel:

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
