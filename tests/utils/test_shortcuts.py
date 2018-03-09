# Third Party Libraries
import pytest
from apistar.exceptions import NotFound
from patients.models import Patient
from utils.shortcuts import get_or_404


class Testget_or_404:
    def test_django_model(self, patient):
        p = get_or_404(Patient, patient.id)
        assert p == patient

    def test_apistar_session(self, patient, ss):
        p = get_or_404(ss.Patient, patient.id)
        assert p == patient

    def test_raise_not_found(self):
        with pytest.raises(NotFound):
            p = get_or_404(Patient, 9999999999)
