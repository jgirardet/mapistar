# Standard Libraries
from typing import TypeVar

# Third Party Libraries
import pendulum
from apistar import Component, exceptions, http
from apistar_jwt.token import JWTUser

# mapistar
# from mapistar.models import db
from mapistar.models import db
from mapistar.utils import get_or_404


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
        today = pendulum.now()
        if not today.is_same_day(self.obj.created):
            raise exceptions.BadRequest(
                "Un acte ne peut être modifié en dehors du jours même"
            )

    def resolve(self, acte_id: http.PathParams, jwt_user: JWTUser) -> ActesPermissions:
        """
        Résolution des permissions

        Args:
            acte_id (dict): dont on extrait le clé `acte_id`

        Returns:
            obj de type :class:`~mapistar.actes.models.Acte`

        Raises:
            Si une permission n'est pas accordée. Exception de type apistar.exceptions
        """
        self.obj = get_or_404(db.Acte, acte_id["acte_id"])
        self.user = jwt_user

        self.only_owner_can_edit()
        self.only_editable_today()

        return self.obj
