from mapistar.utils.shortcuts import get_or_404
import pytest
from apistar.exceptions import NotFound

# Test get_or_404


@pytest.mark.pony
def test_cli_get_patient_404(ponydb):
    with pytest.raises(NotFound):
        get_or_404(ponydb.Patient, 9999)


@pytest.mark.pony
def test_cli_get_patient_ok(ponydb, patient):
    r = get_or_404(ponydb.Patient, patient.pk)
    assert r == ponydb.Patient[patient.pk]
