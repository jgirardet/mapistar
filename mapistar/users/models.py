# Standard Libraries
import typing

# Third Party Libraries
from apistar.backends.django_orm import Session
from apistar.interfaces import Auth
from django.contrib.auth.models import AbstractUser
from django.db import models

STATUT = ['docteur', 'secrétaire', 'interne', 'remplaçant']


class User(AbstractUser):
    """
    Base User class for unolog
    define statu
    """
    MEDECIN = "medecin"
    SECRETAIRE = "secretaire"
    INTERNE = "interne"
    REMPLACANT = "remplacant"
    STATUT = (
        (MEDECIN, 'Médecin'),
        (SECRETAIRE, 'Secrétaire'),
        (INTERNE, "Interne"),
        (REMPLACANT, "Remplaçant"),
    )

    statut = models.CharField(max_length=20, choices=STATUT)


"""
RPPS
ADELI


https://github.com/codingforentrepreneurs/srvup-rest-framework/blob/master/src/accounts/models.py
"""
