from .views import VObs, VPrescriptionLibre

actes_urls = [
    *VObs.urls(),
    *VPrescriptionLibre.urls(),
]
