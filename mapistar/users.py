# Third Party Libraries
import random
from typing import Union

import pendulum
from apistar import Component, Include, Route, exceptions, http, types, validators
from apistar_jwt import JWTUser
from apistar_jwt.decorators import anonymous_allowed
from apistar_jwt.token import JWT
from pony import orm
from werkzeug.security import check_password_hash, generate_password_hash
from apistar_jwt import JWTUser
from mapistar.utils import get_or_404
import random

# mapistar
from mapistar.base_db import db
from mapistar.exceptions import MapistarForbidden
from mapistar.utils import DicoMixin, get_or_404

STATUT = ["docteur", "secrétaire", "interne", "remplaçant"]


class UserPermissions(db.Entity):
    user = orm.Required("User")
    del_patient = orm.Required(bool, default=False)


class User(db.Entity, DicoMixin):
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

    @property
    def dico(self):
        """dico with password hidden"""
        dico = super().dico
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
            raise exceptions.Forbidden("L'ancien mot de passe de correspond pas")

        if new1 != new2:
            raise exceptions.Forbidden("Les mots de passes ne correspondent pas")

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


class UserComponent(Component):
    def resolve(self, user: JWTUser) -> User:
        return get_or_404(User, user.id)


class LoginSchema(types.Type):
    username = validators.String(max_length=100)
    password = validators.String(max_length=100)


@anonymous_allowed
def login(credentials: LoginSchema, jwt: JWT) -> str:
    """
    View d'authentification

    Args:
        credentials: credentials username/password
        jwt: JWT componement pour l'encodage du payload

    Toutes les erreurs "raise"

    Returns:
        token
    """

    user = db.User.get(username=credentials["username"])

    if not user or not user.check_password(credentials["password"]):
        raise exceptions.Forbidden("Incorrect username or password.")

    if not user.actif:
        raise exceptions.Forbidden("Utilisateur inactif")

    payload = {
        "id": user.id,
        "username": user.username,
        "iat": pendulum.now(),
        "exp": pendulum.now() + pendulum.Duration(seconds=1000),
    }
    token = jwt.encode(payload)
    if token is None:
        raise exceptions.ConfigurationError("échec de l'encodage jwt")

    return token


class ChangePaswordSchema(types.Type):
    old = validators.String()
    new1 = validators.String(max_length=100)
    new2 = validators.String(max_length=100)


def change_password(pwd: ChangePaswordSchema, user: JWTUser) -> dict:
    """
    Update users password
    """
    user = get_or_404(User, user.id)
    user.change_password(**pwd)
    return {"msg": "password changed"}


def get_new_password(user: JWTUser) -> dict:
    user = get_or_404(User, user.id)
    return {"password": user.get_new_password()}


class NewUserSchema(types.Type):
    username = validators.String()
    password = validators.String()
    nom = validators.String()
    prenom = validators.String()
    statut = validators.String(enum=STATUT)
    actif = validators.Boolean(default=False)


def create_user(
    data: NewUserSchema, user: User
) -> Union[http.JSONResponse, http.HTMLResponse]:
    """ajouter un nouvel utilisateur"""

    if user.is_admin:
        user = db.User.create_user(**data)
        return http.JSONResponse(user.dico, status_code=201)
    else:
        raise MapistarForbidden("Seul un admin peut ajouter un utilisateur")


routes_users = Include(
    url="/users",
    name="users",
    routes=[
        Route(url="/login/", method="POST", handler=login, name="login"),
        Route(url="/change_password/", method="POST", handler=change_password),
        Route(url="/get_new_password/", method="GET", handler=get_new_password),
        # Route(url="/{id}/", method="PUT", handler=update),
        # # Route(url="/patients/", method="DELETE", handler=delete),
        # Route(url="/{id}/", method="DELETE", handler=delete),
        Route(url="/create_user/", method="POST", handler=create_user),
    ],
)

"""
# MEDECIN = "medecin"
# SECRETAIRE = "secretaire"
# INTERNE = "interne"
# REMPLACANT = "remplacant"
# STATUT = (
#     (MEDECIN, 'Médecin'),
#     (SECRETAIRE, 'Secrétaire'),
#     (INTERNE, "Interne"),
#     (REMPLACANT, "Remplaçant"),
# )

RPPS
ADELI
"""
