# Third Party Libraries
import pendulum
import typing
from apistar import Include, Route, exceptions, Component, http
from apistar_cerberus import ApistarValidator
from apistar_jwt.token import JWT, JWTUser
from apistar_jwt.decorators import anonymous_allowed
from pony import orm
from werkzeug.security import check_password_hash, generate_password_hash

# mapistar
from mapistar.base_db import db


STATUT = ["docteur", "secrétaire", "interne", "remplaçant"]


class User(db.Entity):
    """Class Utilisateur Principale

    blabla

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


Login = ApistarValidator(
    {"username": {"type": "string"}, "password": {"type": "string"}}
)


@anonymous_allowed
def login(cred: Login, jwt: JWT) -> str:
    """
    View d'authentification

    Args:
        cred: credentials username/password
        jwt: JWT componement pour l'endocdage du payload

    Toutes les erreurs "raise"

    Returns:
        token type str
    """

    user = User.get(username=cred["username"])

    if not user or not user.check_password(cred["password"]):
        raise exceptions.Forbidden("Incorrect username or password.")

    if not user.actif:
        print("forb")
        raise exceptions.Forbidden("Utilisateur inactif")

    payload = {
        "user": user.pk,
        "username": user.username,
        "iat": pendulum.now(),
        "exp": pendulum.now() + pendulum.Duration(seconds=5),
    }
    token = jwt.encode(payload)
    if token is None:
        raise exceptions.ConfigurationError("échec de l'encodage jwt")

    return token


class IsAuthenticated:
    """
    Hook qui force l'authentification de toute les requêtes
    """

    def on_request(self, jwt_user: JWTUser):
        """
        Args:
            jwt_user: Force l'exécution du componement JWTUser.

        Raises:
            Si échec de l'authentification
        """


class Permission:
    pass


class ActeWritePermissions(Component):
    """
    Component gérant les permissions des actes
    """

    def resolve(
        self, acte_pk: http.PathParams, jwt_user: JWTUser, rq: Route
    ) -> Permission:

        # obj = get_or_404(self.actesviews.model, obj_id)

        # if obj.created.date() != timezone.now().date():
        #     raise BadRequest("Observation can't be edited another day")

        # if auth.user != obj.owner:
        #     raise Forbidden('Only owner can edit an Observation')

        return acte_pk


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
