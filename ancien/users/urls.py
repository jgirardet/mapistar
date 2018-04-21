# Third Party Libraries
from apistar import Route

from .views import login

users_urls = [
    # Route('/{patient_id}/', 'GET', patients_detail),
    Route('/', 'POST', login),
    #     Route('/{patient_id}/', 'PUT', patients_update),
    #     Route('/', 'GET', patients_list),
]
