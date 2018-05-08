# from mapistar.db import db
from mapistar.utils import get_or_404


class MonC():
    b = "pùplùplùpl"
    updatables = "mokm"

    def bla(self):
        a = get_or_404("model", "rien")
        return a


def test_with_object(mocker):
    with mocker.patch.object(MonC, "bla"):
        MonC.bla.return_value = "11"
        e = MonC()
        assert e.bla() == "11"


def test_with_func(mocker):
    with mocker.patch(
        "tests.test_sand.get_or_404", new=mocker.MagicMock(return_value="11")
    ):
        # mo.return_value = "11"
        e = MonC()
        assert e.bla() == "11"


# from pytest_mock import mocker
from unittest.mock import patch, MagicMock


@patch("tests.test_sand.get_or_404", new=MagicMock(return_value="11"))
def test_func_deco():
    # mo.return_value = "11"
    e = MonC()
    assert e.bla() == "11"


def test_func_with():
    with patch("tests.test_sand.get_or_404", new=MagicMock(return_value="11")):
        # mo.return_value = "11"
        e = MonC()
        assert e.bla() == "11"


def test_func_with_as():
    with patch("tests.test_sand.get_or_404") as mo:
        mo.return_value = "11"
        e = MonC()
        assert e.bla() == "11"


# import tests


def test_mocker_func_with_as(mocker):
    mocker.patch("tests.test_sand.get_or_404", new=mocker.MagicMock(return_value="11"))
    # tests.test_sand.get_or_404.return_value = "11"
    e = MonC()
    assert e.bla() == "11"
