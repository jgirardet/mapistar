# Third Party Libraries
import pytest
from tests.factories import FacPrescriptionLibre

pytestmark = pytest.mark.django_db


# @pytest.mark.timeit(n=1, r=1)
class TestObservation:
    """
    Class to test observtion model
    """

    # observation = FacObservation()
    # @pytest.mark.timeit(n=1, r=1)
    def test_string(self, observation):
        # test __str__
        obs = observation()
        assert str(obs) == obs.motif

    def test_save(self, observation):
        obs = observation()
        import time
        time.sleep(1 / 100)
        obs.save()
        assert obs.created < obs.modified

    def test_update(self, observation):
        obs = observation()
        with pytest.raises(AssertionError):
            obs.update(**{'save': "nmnmlnmlkkl"})


class TestPrescriptionLibre:
    def test_string(self):
        a = FacPrescriptionLibre()
        assert str(a) == a.titre
