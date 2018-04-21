# Standard Libraries
import inspect

# Third Party Libraries
import pendulum
from apistar import Component, Include, Route, exceptions, http, types, validators
from apistar_jwt.decorators import anonymous_allowed
from apistar_jwt.token import JWT, JWTUser
from pony import orm
from werkzeug.security import check_password_hash, generate_password_hash

# mapistar
from mapistar.base_db import db
from mapistar.exceptions import MapistarProgrammingError
from mapistar.shortcuts import get_or_404

STATUT = ["docteur", "secrétaire", "interne", "remplaçant"]


class User(db.Entity):
    """Class Utilisateur Principale

    Attributes:
        pk (int): primary key.
        username (str): Identifiant utilisteur.
        password (str): Mot de passe. Ne doit pas être modifié directement
        nom (str): Nom de l'utilisteur.
        prenom (str): Prénom de l'utilisateur.
        actes (:obj:`orm.Set`): Ensemble des actes pratiqués par l'utilisateur.
        actif (bool): L'utilisateur doit être actif pour accéder au site.  default=True.

    """

    pk = orm.PrimaryKey(int, auto=True)
    username = orm.Required(str, unique=True)
    password = orm.Required(str)
    nom = orm.Required(str)
    prenom = orm.Required(str)
    actes = orm.Set("Acte")
    actif = orm.Required(bool, default=True)

    def __repr__(self):
        """
        nice printing Firstname Name
        """
        return f"[User: {self.prenom} {self.nom}]"

    def check_password(self, password: str) -> bool:
        """ Compare un mot de passe donné au mot de passe enregistré.

        Args:
            password : mot de passe vérifié

        Returns:
            True si ok sinon False
        """

        return check_password_hash(self.password, password)

    @classmethod
    def create_user(
        cls, username: str, password: str, nom: str, prenom: str, actif: bool = True
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
            username=username, password=pwd, nom=nom, prenom=prenom, actif=actif
        )
        return user


class LoginSchema(types.Type):
    username = validators.String(max_length=100)
    password = validators.String(max_length=100)


@anonymous_allowed
def login(credentials: LoginSchema, jwt: JWT) -> str:
    """
    View d'authentification

    Args:
        cred: credentials username/password
        jwt: JWT componement pour l'encodage du payload

    Toutes les erreurs "raise"

    Returns:
        token
    """

    user = User.get(username=credentials["username"])

    if not user or not user.check_password(credentials["password"]):
        raise exceptions.Forbidden("Incorrect username or password.")

    if not user.actif:
        raise exceptions.Forbidden("Utilisateur inactif")

    payload = {
        "id": user.pk,
        "username": user.username,
        "iat": pendulum.now(),
        "exp": pendulum.now() + pendulum.Duration(seconds=5),
    }
    token = jwt.encode(payload)
    if token is None:
        raise exceptions.ConfigurationError("échec de l'encodage jwt")

    return token


routes_users = Include(
    url="/users",
    name="users",
    routes=[
        Route(url="/login/", method="POST", handler=login, name="login"),
        # Route(url="/", method="GET", handler=liste),
        # Route(url="/{pk}/", method="PUT", handler=update),
        # # Route(url="/patients/", method="DELETE", handler=delete),
        # Route(url="/{pk}/", method="DELETE", handler=delete),
        # Route(url="/{pk}/", method="GET", handler=get),
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
