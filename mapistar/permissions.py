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
ActesPermissions = TypeVar("ActesPermissions")
"""Type ActePermissions"""


class ActesPermissionsComponent(Component):
    """
    Component gérant les permissions des actes

    On ajoute les permissions dans :attr:`resolve`::

        self.only_owner_can_edit()
        self.my_new_method()
        ...

    """

    def only_owner_can_edit(self):
        """
        Permission où seul l'utilisateur ayant créé l'acte peut le modifier.
        """
        if self.user.id != self.obj.owner.id:
            raise exceptions.Forbidden(
                "Un utilisateur ne peut modifier un acte créé par un autre utilisateur"
            )

    def only_editable_today(self):
        """
        Permission où le jour de modification doit correspondre au jour de création.
        """
        today = pendulum.now(settings.TZ)
        created = pendulum.instance(self.obj.created).in_tz(settings.TZ)
        if not today.is_same_day(created):
            raise exceptions.BadRequest(
                "Un acte ne peut être modifié en dehors du jours même"
            )

    def run_actes_permissions(self):
        self.only_owner_can_edit()
        self.only_editable_today()

    def resolve(self, params: http.PathParams, jwt_user: JWTUser) -> ActesPermissions:
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

                self.obj = get_or_404(db.Acte, acte_id)

        if item_id:
            self.item = get_or_404(db.Item, item_id)
            self.obj = self.item.ordonnance

        self.user = jwt_user

        self.run_actes_permissions()

        return getattr(self, "item", self.obj)
