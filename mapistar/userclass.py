# Third Party Libraries
import random

import falcon


# mapistar
from mapistar.base_db import db
from pony import orm
from werkzeug.security import check_password_hash, generate_password_hash


STATUT = ["docteur", "secrétaire", "interne", "remplaçant"]


class UserPermissions(db.Entity):
    user = orm.Required("User")
    del_patient = orm.Required(bool, default=False)


class User(db.Entity):
    """
    Entity Utilisateur

    Attributes:
        username (str): Identifiant utilisteur.
        password (str): Mot de passe. Ne doit pas être modifié directement
        nom (str): Nom de l'utilisteur.
        prenom (str): Prénom de l'utilisateur.
        actes (:obj:`orm.Set`): Ensemble des actes pratiqués par l'utilisateur.
        actif (bool): L'utilisateur doit être actif pour accéder au site.  default=True.

    """

    username = orm.Required(str, unique=True)
    password = orm.Required(str)
    nom = orm.Required(str)
    prenom = orm.Required(str)
    actes = orm.Set("Acte")
    actif = orm.Required(bool, default=False)
    statut = orm.Required(str, py_check=lambda x: x in STATUT)
    permissions = orm.Optional(UserPermissions)
    is_admin = orm.Required(bool, default=False)

    def __repr__(self):
        """
        nice printing Firstname Name
        """
        return f"[User: {self.prenom} {self.nom}]"

    # @property
    def to_dict(self):
        """to_dict with password hidden"""
        dico = super().to_dict()
        dico["password"] = "xxxxxxxxxx"
        return dico

    def check_password(self, password: str) -> bool:
        """ Compare un mot de passe donné au mot de passe enregistré.

        Args:
            password : mot de passe vérifié

        Returns:
            True si ok sinon False
        """

        return check_password_hash(self.password, password)

    def before_insert(self):
        UserPermissions(user=self)

    @classmethod
    def create_user(
        cls,
        username: str,
        password: str,
        nom: str,
        prenom: str,
        statut: str,
        actif: bool = True,
        is_admin: bool = False,
    ) -> "User":
        """ Ajoute un utilisateur

        Args:
            username: Identifiant voulu
            password: mot de passe
            nom: Nom de l'utilisateur
            prenom: Prenom de l'utilisateur
            actif: Actif par défaut

        Returns:
            Nouvel utilisateur
        """
        pwd = generate_password_hash(password)
        user = db.User(
            username=username,
            password=pwd,
            nom=nom,
            prenom=prenom,
            statut=statut,
            actif=actif,
            is_admin=is_admin,
        )
        return user

    def change_password(self, old, new1, new2):
        if not self.check_password(old):
            raise falcon.HTTPForbidden(title="L'ancien mot de passe de correspond pas")

        if new1 != new2:
            raise falcon.HTTPForbidden(title="Les mots de passes ne correspondent pas")

        self.pwd = generate_password_hash(new1)

    def get_new_password(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw_length = 10
        mypw = ""

        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypw = mypw + alphabet[next_index]

        self.password = mypw
        return mypw
