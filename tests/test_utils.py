import pytest

from mapistar.utils import get_or_404, PendulumDateTime, DicoMixin
from apistar import exceptions
from unittest.mock import MagicMock
from datetime import datetime, date
import pendulum

pytestmark = pytest.mark.pony


pd = PendulumDateTime()


def test_pendulum_datetime():
    # set_name
    pd.__set_name__("owner", "lenom")
    assert pd.field == "_lenom"

    # get
    instance = MagicMock()
    instance._lenom = datetime(2007, 12, 5, 12, 12)
    a = pd.__get__(instance, "owner")
    assert a == pendulum.DateTime(2007, 12, 5, 12, 12).in_tz("UTC")

    # set
    # peut échouer au
    a = pendulum.DateTime(2007, 12, 5, 12, 12, tzinfo=pendulum.timezone("Europe/Paris"))
    pd.__set__(instance, a)
    assert instance._lenom == a.in_tz("UTC").naive()


def test_get_or_404_pass_int_and_string(observation):
    a = get_or_404(observation.__class__, int(observation.id))
    assert a.id is not None
    a = get_or_404(observation.__class__, str(observation.id))
    assert a.id is not None


def test_get_or_404_not_found(observation):
    with pytest.raises(exceptions.NotFound):
        get_or_404(observation.__class__, 999)


def test_dico():
    d = DicoMixin()
    d.to_dict = MagicMock(return_value={"aze": "aze", "nb": 1})
    # field not modified
    assert {"aze": "aze", "nb": 1} == d.dico

    # datetime
    dt = datetime(2018, 4, 22, 19, 10, 19, 695600)
    d.created = pendulum.instance(dt)
    d.to_dict = MagicMock(return_value={"aze": "aze", "nb": 1, "_created": dt})
    assert d.dico["created"] == "2018-04-22T19:10:19.695600+00:00"
    assert "_created" not in d.dico
    # date
    dt = date(2018, 4, 22)
    d.created = dt
    d.to_dict = MagicMock(return_value={"aze": "aze", "nb": 1, "created": dt})
    assert d.dico["created"] == "2018-04-22"
