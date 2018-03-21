from .actesviews import ActesViews
from .models import Observation, PrescriptionLibre

VObs = ActesViews(Observation)
VPrescriptionLibre = ActesViews(PrescriptionLibre)
