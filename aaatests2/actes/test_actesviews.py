# Standard Libraries

# Third Party Libraries
import pytest
from actes.actesviews import ActesViews
from actes.models import Observation
from actes.schemas.observation import ObservationSchema, ObservationUpdateSchema
from apistar.exceptions import BadRequest
from django.utils import timezone
from tests.factories import FacUser

Vobs = ActesViews(Observation)


# init
def test_init():
    assert Vobs.model == Observation
    assert Vobs.url_name == "observations"


# create
def test_observation_create(patient, ss, auth_user):
    req = {"patient_id": patient.id, "motif": "blabla"}
    rep = Vobs.create()(req, auth_user, ss)
    assert rep.status == 201


# update
def test_observation_update(observation, ss, user, auth_user):
    obs = observation(owner=user)
    params = ObservationUpdateSchema({'motif': "blabla"})
    o = Vobs.update()(obs.id, params, auth_user)
    od_db = ss.Observation.objects.get(id=obs.id)
    assert o.content['motif'] == "blabla" == od_db.motif


@pytest.mark.parametrize('params', [{}, {'motidzdzdf': "blabla"}])
def test_observation_update_bad_new_data(params, observation, ss, user,
                                         auth_user):
    obs = observation(owner=user)
    with pytest.raises(BadRequest):
        Vobs.update()(obs.id, params, auth_user)


# delete
def test_observation_delete(observation, auth_user):
    obs = observation(owner=auth_user.user)
    o = Vobs.delete()(obs.id, auth_user)
    assert o.status == 201


def test_list_acte_pass(patient, observation):
    obss = [observation(patient=patient) for i in range(5)]
    req = Vobs.liste()(patient.id)
    assert req == [ObservationSchema(item) for item in obss][::-1]


# get_one
def test_get_one_acte_pass(observation, patient):
    obss = observation(patient=patient)
    req = Vobs.get_one()(obss.id)
    assert obss.id == req['id']
