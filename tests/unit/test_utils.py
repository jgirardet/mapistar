from datetime import date, datetime
from unittest.mock import MagicMock

import pytest
from apistar import exceptions
from pony.orm import ObjectNotFound

from mapistar.exceptions import MapistarProgrammingError
from mapistar.utils import (
    DicoMixin,
    NameMixin,
    check_config,
    get_or_404,
    import_models,
    SetMixin,
)


class TestCheckConfg:
    def test_jwt_duration(self, mocker):
        s = mocker.MagicMock(**{"JWT_DURATION": None})
        with pytest.raises(MapistarProgrammingError) as exc:
            check_config(s)
        assert str(exc.value) == "La durée des JWT doit être précisée"


class TestImportModels:
    def test_arg_format(self):
        a = ([],)
        with pytest.raises(MapistarProgrammingError) as exc:
            import_models(a)
        assert (
            str(exc.value)
            == "Déclaration de module sous la forme str ou tuple('base', ('module1','modele2'))"
        )

    def test_insinstance_str(self, mocker):
        call = mocker.call
        models = ("actes", "observations", "ordonnances", "ordo_items")
        r = mocker.patch("importlib.import_module")
        import_models(models)
        calls = [
            call("mapistar.actes"),
            call("mapistar.observations"),
            call("mapistar.ordonnances"),
            call("mapistar.ordo_items"),
        ]
        r.assert_has_calls(calls)

    def test_insinstance_tuple(self, mocker):
        call = mocker.call
        models = [("actes", ("observations", "ordonnances", "ordo_items"))]
        r = mocker.patch("importlib.import_module")
        import_models(models)
        calls = [
            call("mapistar.actes.observations"),
            call("mapistar.actes.ordonnances"),
            call("mapistar.actes.ordo_items"),
        ]
        r.assert_has_calls(calls)


def test_get_or_404_pass(mocker):

    entity = mocker.MagicMock()
    entity.__getitem__.return_value = 1
    a = get_or_404(entity, 12)

    entity.__getitem__.assert_called_with(12)
    assert a == 1


def test_get_or_404_not_found(mocker):
    entity = mocker.MagicMock()
    ett = mocker.MagicMock(**{"__name__": "irne"})
    entity.__getitem__ = mocker.MagicMock(side_effect=ObjectNotFound(ett))

    with pytest.raises(exceptions.NotFound):
        get_or_404(entity, 999)


def test_dico():
    d = DicoMixin()
    d.to_dict = MagicMock(return_value={"aze": "aze", "nb": 1})
    # field not modified
    assert {"aze": "aze", "nb": 1} == d.dico

    # datetime
    dt = datetime(2018, 4, 22, 19, 10, 19, 695600)
    d.created = dt
    d.to_dict = MagicMock(return_value={"aze": "aze", "nb": 1, "created": dt})
    assert d.dico["created"] == "2018-04-22T19:10:19.695600"
    # date
    dt = date(2018, 4, 22)
    d.created = dt
    d.to_dict = MagicMock(return_value={"aze": "aze", "nb": 1, "created": dt})
    assert d.dico["created"] == "2018-04-22"


def test_set_mixin(mocker):
    a = MagicMock()
    a.updatable = ("un", "deux", "trois")
    g = mocker.patch("builtins.super")
    h = g.return_value
    SetMixin.set(a, **{"un": 1, "trois": 3})
    mocker.stopall()

    h.set.assert_called_with(un=1, trois=3)

    a.updatable = ("un", "deux")
    with pytest.raises(AttributeError) as exc:
        SetMixin.set(a, **{"un": 1, "trois": 3})
    assert str(exc.value) == "trois n'est pas updatable"


def test_name_mixin(mocker):
    m = NameMixin
    m.__name__ = "Hello"
    assert m.__name__ == "Hello"
    assert m.name == "Hello"
    assert m.url_name == "hellos"

    m.__name__ = "Hellos"
    assert m.name == "Hellos"
    assert m.url_name == "hellos"
    m.__name__ = "Hellox"
    assert m.name == "Hellox"
    assert m.url_name == "hellox"
    # assert NameMixin.name(m) == "NameMixin"
    # assert m.url_name == "namemixins"
    # assert type(m.__name__) == "1"
