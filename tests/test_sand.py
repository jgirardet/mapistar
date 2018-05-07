# from mapistar.db import db


class Meta(type):

    def __new__(meta, name, bases, dico):

        obj = type.__new__(meta, name, bases, dico)

        obj.routes  = {'route1':obj.add()}

        return obj
        # return type.__new__(meta, name, bases, dico)


class MyClass(metaclass=Meta):

    model = None
    updatables = None
    schemas = None
    # return type.__new__(name, base, dico)

    @classmethod
    def add(cls):

        def add():
            return cls.schemas

        return add


schema1 = "schema1"
schema2 = "schema2"


class MonC(MyClass):
    b = "pùplùplùpl"
    updatables = "mokm"
    schemas = [schema1, schema2]


def test_mon():
    # e = MyClass()
    print(MonC.routes)
    assert True
