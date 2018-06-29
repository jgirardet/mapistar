from datetime import date, datetime
from unittest.mock import MagicMock

import pytest
from falcon import HTTPNotFound
from pony.orm import ObjectNotFound

from mapistar.exceptions import MapistarProgrammingError
from mapistar.utils import (
    NameMixin,
    check_config,
    get_or_404,
    import_models,
    SetMixin,
    CapWordsMixin,
)


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

    with pytest.raises(HTTPNotFound) as e:
        get_or_404(entity, 999)

    assert e.value.title == "Aucun MagicMock trouvé avec l'id 999"
