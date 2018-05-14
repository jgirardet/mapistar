# Standard Libraries
from typing import TypeVar

# Third Party Libraries
import pendulum
from apistar import Component, exceptions, http
from apistar_jwt.token import JWTUser
from simple_settings import settings

# mapistar
# from mapistar.db import db
from mapistar.base_db import db
from mapistar.utils import get_or_404
from mapistar.exceptions import MapistarProgrammingError


class IsAuthenticated:
    """
    Hook qui force l'authentification de toute les requêtes
    """

    def on_request(self, jwt_user: JWTUser) -> None:
        """
        Args:
            jwt_user: Force l'exécution du componement JWTUser.

        Raises:
            Si échec de l'authentification
        """


# ActesPermissions = type("ActesPermissions", (), {})
# ActesPermissions = TypeVar("ActesPermissions")
# """Type ActePermissions"""
class ActesPermissions:
    """
    Class regroupant les permissions et leur éxecutions

    Args:
        acte: Acte testé en permission
        user: User testé en permission

    Raises:
        Si un permission n'est pas correct
    """

    def __init__(self, acte, user):
        self.acte = acte
        self.user = user

    def __call__(self):
        """
        teste tous les permissions
        """

        self.only_owner_can_edit()
        self.only_editable_today()

    def only_owner_can_edit(self):
        """
        Permission où seul l'utilisateur ayant créé l'acte peut le modifier.
        """
        if self.user.id != self.acte.owner.id:
            raise exceptions.Forbidden(
                "Un utilisateur ne peut modifier un acte créé par un autre utilisateur"
            )

    def only_editable_today(self):
        """
        Permission où le jour de modification doit correspondre au jour de création.
        """
        today = pendulum.now(settings.TZ)
        created = pendulum.instance(self.acte.created).in_tz(settings.TZ)
        if not today.is_same_day(created):
            raise exceptions.BadRequest(
                "Un acte ne peut être modifié en dehors du jours même"
            )


class ActesPermissionsComponent(Component):
    """
    Component associant les permissions

    """

    def resolve(self, params: http.PathParams, user: JWTUser) -> ActesPermissions:
        """
        Résolution des permissions

        Args:
            params (dict): dont on extrait le clé `acte_id` et `item_id`

        Returns:
            obj de type :class:`~mapistar.actes.models.Acte` ou :class:`~mapistar.actes.ordo_items.Item`

        Raises:
            Si une permission n'est pas accordée. Exception de type apistar.exceptions
        """
        acte_id = params.get("acte_id", None)
        item_id = params.get("item_id", None)

        if acte_id:
            if item_id:
                raise MapistarProgrammingError(
                    "Une requête ne peut spécifier item_id et acte_id à la fois"
                )

            else:
                acte = obj = get_or_404(db.Acte, acte_id)

        elif item_id:
            obj = get_or_404(db.Item, item_id)
            acte = obj.ordonnance
        else:
            raise MapistarProgrammingError("doit préciser acte_id ou item_id")

        ActesPermissions(acte, user)()

        return obj
