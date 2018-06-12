from pony.orm import Optional, Required, Set
from mapistar.utils import DicoMixin, CapWordsMixin
from mapistar.base_db import db

# from mapistar.actes.avis import Avis

MAX_LENGTH = {
    "nom": 100,
    "prenom": 100,
    "rue": 200,
    "ville": 100,
    "tel": 20,
    "email": 100,
}
""" Valeurs maximales pour chaque field"""


MAX = {"cp": 10000000}


class Praticien(CapWordsMixin, DicoMixin, db.Entity):
    """
    Entity Praticien

    Attributes:
        nom (str): Nom du praticien. Requis
        prenom (str): prenom du praticien. Requis
        rue (str): Rue
        cp(int): Code Postal
        ville(str): Ville
        tel(str): Téléphone
        portable(str): Téléphone portable
        email(str): E-mail
        actes(mapistar.actes.models.Acte): Actes ratachés au praticien.

    """

    nom = Required(str, MAX_LENGTH["nom"])
    prenom = Required(str, MAX_LENGTH["prenom"])
    rpps = Optional(int)
    rue = Optional(str, MAX_LENGTH["rue"])
    cp = Optional(int, max=MAX["cp"])
    ville = Optional(str, MAX_LENGTH["ville"])
    tel = Optional(str, MAX_LENGTH["tel"])
    portable = Optional(str, MAX_LENGTH["tel"])
    email = Optional(str, MAX_LENGTH["email"])

    avis = Set("Avis")

    def __repr__(self):
        """
        nice printing Firstname Name
        """
        return f"[Praticien: {self.prenom} {self.nom}]"


# class PraticienCreateSchema(types.Type):
#     nom = validators.String(max_length=MAX_LENGTH["nom"])
#     prenom = validators.String(max_length=MAX_LENGTH["prenom"])
#     ddn = validators.Date()
#     sexe = validators.String(
#         description="sexe", max_length=MAX_LENGTH["sexe"], enum=SEXE
#     )


# class PraticienUpdateSchema(types.Type):
#     nom = validators.String(max_length=MAX_LENGTH["nom"], default="")
#     prenom = validators.String(max_length=MAX_LENGTH["prenom"], default="")
#     rue = validators.String(description="rue", max_length=MAX_LENGTH["rue"], default="")
#     cp = validators.Integer(description="Code Postal", default=None, allow_null=True)
#     ville = validators.String(
#         description="Ville", max_length=MAX_LENGTH["ville"], default=""
#     )
#     tel = validators.String(
#         description="Numéro de Téléphone", max_length=MAX_LENGTH["tel"], default=""
#     )
#     portable = validators.String(
#         description="Numéro de Téléphone Portable",
#         max_length=MAX_LENGTH["tel"],
#         default="",
#     )
#     email = validators.String(
#         description="email", max_length=MAX_LENGTH["email"], default=""
#     )


# 0 Type d'identifiant PP
# 1 Identifiant PP
# 2 Identification nationale PP
# 3 Code civilité d'exercice
# 4 Libellé civilité d'exercice
# 5 Code civilité
# 6 Libellé civilité
# 7 Nom d'exercice
# 8 Prénom d'exercice
# 9 Code profession
# 10 Libellé profession
# 11 Code catégorie professionnelle
# 12 Libellé catégorie professionnelle
# 13 Code type savoir-faire
# 14 Libellé type savoir-faire
# 15 Code savoir-faire
# 16 Libellé savoir-faire
# 17 Code mode exercice
# 18 Libellé mode exercice
# 19 Numéro SIRET site
# 20 Numéro SIREN site
# 21 Numéro FINESS site
# 22 Numéro FINESS établissement juridique
# 23 Identifiant technique de la structure
# 24 Raison sociale site
# 25 Enseigne commerciale site
# 26 Complément destinataire (coord. structure)
# 27 Complément point géographique (coord. structure)
# 28 Numéro Voie (coord. structure)
# 29 Indice répétition voie (coord. structure)
# 30 Code type de voie (coord. structure)
# 31 Libellé type de voie (coord. structure)
# 32 Libellé Voie (coord. structure)
# 33 Mention distribution (coord. structure)
# 34 Bureau cedex (coord. structure)
# 35 Code postal (coord. structure)
# 36 Code commune (coord. structure)
# 37 Libellé commune (coord. structure)
# 38 Code pays (coord. structure)
# 39 Libellé pays (coord. structure)
# 40 Téléphone (coord. structure)
# 41 Téléphone 2 (coord. structure)
# 42 Télécopie (coord. structure)
# 43 Adresse e-mail (coord. structure)
# 44 Code Département (structure)
# 45 Libellé Département (structure)
# 46 Ancien identifiant de la structure
# 47 Autorité d'enregistrement
