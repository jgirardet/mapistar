# Third Party Libraries
import pytest

from . import factory


@pytest.fixture(scope="function")
def patient():
    """ patient """
    return factory.patientf()


@pytest.fixture(scope="function")
def user(request):
    return factory.userf()


@pytest.fixture(scope="function")
def acte(request):
    return factory.actef()


@pytest.fixture(scope="function")
def observation(request):
    return factory.observationf()


@pytest.fixture(scope="function")
def ordonnance(request):
    return factory.ordonnancef()


@pytest.fixture(scope="function")
def item(request, ordonnance):
    return factory.itemf(ordonnance=ordonnance)


@pytest.fixture(scope="function")
def medicament(request):
    return factory.medicamentf()
