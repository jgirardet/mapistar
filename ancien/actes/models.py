# Third Party Libraries
from django.conf import settings
from django.db import models
from django.utils import timezone
from patients.models import Patient


class BaseActe(models.Model):
    """
    Base Abstract class for for differnets actions
    made by users
    Updatable fields by user must be set in updatable
    """
    patient = models.ForeignKey(Patient, related_name="%(class)ss", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="%(class)ss", on_delete=models.PROTECT)

    updatable = []

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super().save(*args, **kwargs)

    def update(self, **kwargs):
        """
        Update depending updatable items
        """
        for k, v in kwargs.items():
            getattr(self, k)  # raise attributeerror if k not in model
            assert k in self.updatable, "k is not in updatable"  # prevent
            setattr(self, k, v)

        self.save()


class Observation(BaseActe):
    """
    A small text of  user about a patient

    motif : purpose of the visit. can't be blank.this is the most minimam
    thing a user schould enter.
    """
    motif = models.CharField(max_length=60, blank=False)
    body = models.TextField(blank=True)

    updatable = ['motif', 'body']

    def __str__(self):
        return self.motif  # no


class PrescriptionLibre(BaseActe):
    """
    small prescirption free
    """
    titre = models.CharField(max_length=60, blank=False)
    body = models.TextField(blank=True)

    updatable = ['titre', 'body']

    def __str__(self):
        return self.titre


"""
BAseActe:
Observation :
    TA/pouls
    conclusion

ordonnance
vaccin
certif
    titre
    texte
courries
    dest
    corps
courriers reçus
    spé
    nom
    contenu
    pdf
examens:
    type
    effecteur
    pdf
REGROUPER courrier et examens ?

bio
antécédants
intolérances
allergies
"""
