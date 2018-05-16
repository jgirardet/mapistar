# Standard Libraries
import json

# Third Party Libraries
import pytest
from tests.factory import ordonnancef

pytestmark = pytest.mark.pony


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


class TestItemViews:

    def test_add(self, ordonnance, cli, app):
        a = {"ordonnance": ordonnance.id, "cip": "1234567890123", "nom": "Un Médoc"}
        r = cli.post(app.reverse_url("medicaments:add_item"), data=json.dumps(a))
        assert r.status_code == 201

    def test_delete_item(self, medicament, cli, app):
        print(medicament.ordonnance.id)

        medicament.ordonnance.owner = cli.user
        r = cli.delete(
            app.reverse_url("medicaments:delete_item", item_id=medicament.id)
        )
        assert r.status_code == 200
