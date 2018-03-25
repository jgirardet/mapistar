# Third Party Libraries
from apistar import types, validators
from pony import orm
import pytest
db = orm.Database()


class A(db.Entity):
    a = orm.Required('B')
    b = orm.Required(str)
    c = orm.Optional(str)


class B(db.Entity):
    aa = orm.Set('A')


db.connect(
    provider="sqlite",
    filename="db.sqlite3",
    create_tables=True,
    create_db=True,
    # allow_auto_upgrade=True,
)


@pytest.mark.pony
def test_use_set():
    b = B()
    a = db.A(a=b, b="lùplùpl")
    print(a.to_dict())
    a.set(**{"b": "omkmokmo"})
    print(a.to_dict())
    assert a.a == b
    assert a.b == "omkmokmo"