# Third Party Libraries
# import pytest
# mapistar
# mapistar
# mapistar
# mapistar
# mapistar
# mapistar
from mapistar.theso import fuzzy


def test_fuzzy(mocker):
    m = mocker.patch("mapistar.theso.theso_session")
    r = fuzzy("bla")

    m.fuzzy.assert_called_with("bla")
    assert r == m.fuzzy.return_value
