from . import factory
import pytest

# pytestmark = pytest.mark.pony


@pytest.fixture(scope='function')
def patient():
    """ patient """
    return factory.patient()


@pytest.fixture(scope='function')
def user(request):
    return factory.user()


@pytest.fixture(scope='function')
def acte(request):
    return factory.acte()


@pytest.fixture(scope='function')
def observation(request):
    return factory.observation()


@pytest.fixture(scope='function')
def ordonnance(request):
    return factory.ordonnance()


@pytest.fixture(scope='function')
def medicament(request):
    return factory.medicament()