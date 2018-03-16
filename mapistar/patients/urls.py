# Third Party Libraries
from apistar import Route

from .views import patients_create, patients_list  #, patients_detail, patients_list, patients_update

patients_urls = [
    # Route('/{patient_id}/', 'GET', patients_detail),
    Route('/', 'POST', patients_create),
    # Route('/{patient_id}/', 'PUT', patients_update),
    Route('/', 'GET', patients_list),
]
