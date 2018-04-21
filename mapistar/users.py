# Standard Libraries
import inspect
from typing import NewType

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


class LoginSchema(types.Type):
    username = validators.String(max_length=100)
    password = validators.String(max_length=100)


@anonymous_allowed
def login(cred: LoginSchema, jwt: JWT) -> str:
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


BasePermissions = type("BasePermissions", (), {})
ActesPermissions = type("ActesPermissions", (BasePermissions,), {})


class PermissionsComponent(Component):
    """
    Component gérant les permissions des actes

    Les classes de permissions sont définies en subclassant BasePermissions::
        MyClassPermissions = type("MyClassPermissions", (BasePermissions,), {})

    On ajoute ensuite les permissions::
        if parameter.annotation is MyClassPermissions:
            self.only_owner_can_edit()
            self.my_new_method()

    """

    def only_owner_can_edit(self):
        """
        Vérifie que seul l'utilisateur ayant créé l'acte puisse le modifier
        """
        if self.user.id != self.obj.owner.pk:
            raise exceptions.Forbidden(
                "Un utilisateur ne peut modifier un acte créé par un autre utilisateur"
            )

    def only_editable_today(self):
        """
        Vérifie que le jour de modification corresponde au jours même
        """
        today = pendulum.now()
        if not today.is_same_day(self.obj.created):
            raise exceptions.BadRequest(
                "Un acte ne peut être modifié en dehors du jours même"
            )

    def can_handle_parameter(self, parameter: inspect.Parameter):
        return issubclass(parameter.annotation, BasePermissions)

    def resolve(
        self, acte_pk: http.PathParams, jwt_user: JWTUser, parameter: inspect.Parameter
    ):
        self.obj = get_or_404(db.Acte, acte_pk["acte_pk"])
        self.user = jwt_user

        if parameter.annotation is ActesPermissions:
            self.only_owner_can_edit()
            self.only_editable_today()

        else:
            raise MapistarProgrammingError(
                f"Permission {parameter.annotation.__name__} non évaluée dans resolve"
            )

        return self.obj




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
