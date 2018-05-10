# Standard Libraries
import json

# Third Party Libraries
import pytest
from pony.orm import OperationWithDeletedObjectError
from tests.factory import itemf, ordonnancef

pytestmark = pytest.mark.pony


class TestOrdonnanceModel:

    def test_dico_super_is_called(self, ordonnance, ponydb):
        for i in range(3):
            ponydb.Item(ordonnance=ordonnance)
        # a.flush()

        dico = ordonnance.dico
        dico.pop("items")
        assert isinstance(dico["created"], str), "confirme l'appel de super()"

    def test_ordre(self, ordonnance, ponydb):
        # ajout simple
        [itemf(ordonnance=ordonnance) for x in range(5)]
        ordre = ordonnance.dico["ordre"]
        assert ordre == "1-2-3-4-5"

        # après delete
        ponydb.Item[2].delete()
        ordre = ordonnance.dico["ordre"]
        assert ordre == "1-3-4-5"

    def test_get_ordered_items(self, ordonnance, ponydb):
        [itemf(ordonnance=ordonnance) for x in range(5)]
        ordre = "3-2-5-1-4"
        ordonnance.ordre = ordre
        ordonnance.dico
        assert [i.id for i in ordonnance.get_ordered_items()] == [3, 2, 5, 1, 4]

        # flallback, bad ordre
        ordre = "3-2-4"
        ordonnance.ordre = ordre
        ordonnance.dico
        assert {i.id for i in ordonnance.get_ordered_items()} == {3, 2, 5, 1, 4}


from tests.factory import ordonnancef


class TestOrdonnanceViews:

    def test_add(self, patient, cli, app):
        a = {"patient": patient.id}
        r = cli.post(app.reverse_url("ordonnances:add"), data=json.dumps(a))
        assert r.status_code == 201

    def test_list_acte_pass(self, patient, app, cli, ponydb):

        ord = [ordonnancef(owner=cli.user, patient=patient) for i in range(3)]
        r = cli.get(app.reverse_url("ordonnances:liste", patient_id=patient.id))
        assert {x["id"] for x in r.json()} == {x.id for x in ord}

    def test_one_pass(self, ordonnance, cli, app):
        r = cli.get(app.reverse_url("ordonnances:one", acte_id=ordonnance.id))
        assert r.status_code == 200
        assert r.json() == ordonnance.dico

    # def test_delete_pass(self, ordonnance, cli, app):

    def test_delete_pass(self, cli, app):
        ordonnance = ordonnancef()
        ordonnance.owner = cli.user
        print(ordonnance.items.select()[:])
        r = cli.delete(app.reverse_url("ordonnances:delete", acte_id=ordonnance.id))
        assert r.status_code == 200

    def test_update_pass(self, cli, app, ordonnance):
        ordonnance.owner = cli.user
        upd = {"ordre": "1-2-3-4-5"}
        r = cli.put(
            app.reverse_url("ordonnances:update", acte_id=ordonnance.id),
            data=json.dumps(upd),
        )
        assert r.status_code == 200
        assert r.json()["ordre"] == "1-2-3-4-5"
