from pony.orm import Optional, Required


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


class Praticien(db.Entity, DicoMixin):
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

    actes = Set("Acte")

    def __repr__(self):
        """
        nice printing Firstname Name
        """
        return f"[Praticien: {self.prenom} {self.nom}]"

    def _capwords(self):
        """
        Majusculise la première lettre
        """

        self.nom = capwords(self.nom)
        self.prenom = capwords(self.prenom)

    def before_insert(self):
        """
        * Nom et Prenom sont Majsuculisés
        """
        self._capwords()

    def before_update(self):
        """
        * Nom et Prénom sont Majsuculisés
        """
        self._capwords()


class PraticienCreateSchema(types.Type):
    nom = validators.String(max_length=MAX_LENGTH["nom"])
    prenom = validators.String(max_length=MAX_LENGTH["prenom"])
    ddn = validators.Date()
    sexe = validators.String(
        description="sexe", max_length=MAX_LENGTH["sexe"], enum=SEXE
    )


class PraticienUpdateSchema(types.Type):
    nom = validators.String(max_length=MAX_LENGTH["nom"], default="")
    prenom = validators.String(max_length=MAX_LENGTH["prenom"], default="")
    rue = validators.String(description="rue", max_length=MAX_LENGTH["rue"], default="")
    cp = validators.Integer(description="Code Postal", default=None, allow_null=True)
    ville = validators.String(
        description="Ville", max_length=MAX_LENGTH["ville"], default=""
    )
    tel = validators.String(
        description="Numéro de Téléphone", max_length=MAX_LENGTH["tel"], default=""
    )
    portable = validators.String(
        description="Numéro de Téléphone Portable",
        max_length=MAX_LENGTH["tel"],
        default="",
    )
    email = validators.String(
        description="email", max_length=MAX_LENGTH["email"], default=""
    )
