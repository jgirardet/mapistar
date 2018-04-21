# Third Party Libraries
from apistar import Link, Section

from .views import add, delete, get, liste, update

section_patients = Section(
    name="patients",
    content=[
        Link(url="/patients/", method="POST", handler=add),
        Link(url="/patients/", method="GET", handler=liste),
        Link(url="/patients/{pk}/", method="PUT", handler=update),
        # Link(url="/patients/", method="DELETE", handler=delete),
        Link(url="/patients/{pk}/", method="DELETE", handler=delete),
        Link(url="/patients/{pk}/", method="GET", handler=get),
    ],
    title="titre de section patieny",
    description="descriptoin Api des patients")

# patients_urls = [
#     # Route('/{patient_id}/', 'GET', patients_detail),
#     Route('/', 'POST', patients_create),
#     # Route('/{patient_id}/', 'PUT', patients_update),
#     Route('/', 'GET', patients_list),
# ]
