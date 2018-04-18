# Standard Libraries
import inspect
import json

# Third Party Libraries
import cerberus
from apistar import App, Route, TestClient
from apistar_cerberus import ApistarValidator, CerberusComp
import pytest

schema = {"a": {"type": "string", "required": True}, "b": {"type": "string"}}

RienCerbCreate = ApistarValidator(schema)
RienCerbUpdate = ApistarValidator(schema, update=True)


def helloCerb(rien: RienCerbCreate):
    return rien


def helloCerbUpdate(rien: RienCerbUpdate):
    return rien


from pony.orm import Database, Required, db_session

db = Database()


class Ee(db.Entity):
    a = Required(str)


db.connect(provider="sqlite", filename=":memory:", create_tables=True)


def add_Ed(rien: RienCerbCreate):
    inst = db.Ee(**rien)
    return inst.to_dict()


routen = Route(url="/n/", method="POST", handler=helloCerb)
routeupdate = Route(url="/update/", method="PUT", handler=helloCerbUpdate)
routeed = Route(url="/eee/", method="POST", handler=add_Ed)

app = App(routes=[routen, routeupdate, routeed], components=[CerberusComp()])

cli = TestClient(app)


@db_session
def test_add_Ee():
    r = cli.post("/eee/", data=json.dumps({"a": "hello Cerberus"}))
    assert r.json() == {"a": "hello Cerberus", "id": 1}


def test_wrong_type():
    rn = cli.post("/n/", data=json.dumps({"a": 1}))
    assert rn.json() == {"a": ["must be of string type"]}


def test_field_required():
    rn = cli.post("/n/", data=json.dumps({"b": "hello Cerberus"}))
    assert rn.json() == {"a": ["required field"]}


def test_good_required_and_not():
    rn = cli.post(
        "/n/", data=json.dumps({"a": "whith required field", "b": "hello Cerberus"})
    )
    assert rn.json() == {"a": "whith required field", "b": "hello Cerberus"}


def test_update_trus_at_instantiate():
    rn = cli.put("/update/", data=json.dumps({"b": "hello Cerberus"}))
    assert rn.json() == {"b": "hello Cerberus"}
