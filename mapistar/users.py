# Third Party Libraries
import pendulum
from apistar import Include, Route, exceptions, types, validators
from apistar_jwt.decorators import anonymous_allowed
from apistar_jwt.token import JWT
from pony import orm
from werkzeug.security import check_password_hash, generate_password_hash
from apistar_jwt import JWTUser
from mapistar.utils import get_or_404

# mapistar
from mapistar.base_db import db

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
    actif = orm.Required(bool, default=True)
    statut = orm.Required(str, py_check=lambda x: x in STATUT)
    permissions = orm.Optional(UserPermissions)

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
        )
        return user

    def change_password(self, old, new1, new2):
        if not self.check_password(old):
            raise exceptions.Forbidden("L'ancien mot de passe de correspond pas")

        if new1 != new2:
            raise exceptions.Forbidden("Les mots de passes ne correspondent pas")

        self.pwd = generate_password_hash(new1)


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

    user = User.get(username=credentials["username"])

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


routes_users = Include(
    url="/users",
    name="users",
    routes=[
        Route(url="/login/", method="POST", handler=login, name="login"),
        Route(url="/change_password/", method="POST", handler=change_password),
        # Route(url="/{id}/", method="PUT", handler=update),
        # # Route(url="/patients/", method="DELETE", handler=delete),
        # Route(url="/{id}/", method="DELETE", handler=delete),
        # Route(url="/{id}/", method="GET", handler=get),
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
