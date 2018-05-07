import json
import pytest

pytestmark = pytest.mark.pony
from tests.factory import medicamentf


class TestMedicamentsViews:

    def test_add(self, ordonnance, cli, app):
        a = {"ordonnance": ordonnance.id, "cip": "1234567890123", "nom": "Un Médoc"}
        r = cli.post(app.reverse_url("medicaments:add"), data=json.dumps(a))
        # # fmt: off
        # import pdb; pdb.set_trace() # fmt: on
        assert r.status_code == 201


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
