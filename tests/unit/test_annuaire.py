import pytest

from mapistar.annuaire import Praticien


class TestModelPraticien:
    def test_capsword_is_called(self, mocker):
        a = mocker.MagicMock(spec=Praticien)
        Praticien.before_update(a)
        a._capwords.assert_called()
