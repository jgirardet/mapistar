# Standard Libraries
import importlib
from datetime import date, datetime
from string import capwords


# Third Party Libraries
from descriptors import classproperty
from pony import orm
from falcon import HTTPNotFound

# mapistar
from mapistar.exceptions import MapistarProgrammingError


def check_config(settings):

    # checl jwt_duration
    if not settings.JWT_DURATION:  # pragma: no cover
        raise MapistarProgrammingError("La durée des JWT doit être précisée")

    if not settings.DOCUMENTS_DIR:  # pragma: no cover
        raise MapistarProgrammingError("STATIC_DIR non configurée")


def import_models(module_liste: list):
    """
    Import tous les modules contenant des Entity ponyorm

    Doit être appelé avant le db.bind()

    Args:
        module_liste: Liste des moduels où se trouvent les Entities Pony.
    """
    modules = {}
    for item in module_liste:
        if isinstance(item, str):
            modules[item] = importlib.import_module(".".join(("mapistar", item)))

        elif isinstance(item, tuple):
            for module in item[1]:
                modules[module] = importlib.import_module(
                    ".".join(("mapistar", item[0], module))
                )
        else:
            raise MapistarProgrammingError(
                "Déclaration de module sous la forme str ou tuple('base', ('module1','modele2'))"
            )

    return modules


def get_or_404(model: orm.core.Entity, id: [str, int]):
    """
    Classique get or raisse http404

    Args:
        model: Modèle sur lequel la requête est effectuée.
        id: identifiant en base de donnée.
    """
    try:
        item = model[id]
    except orm.ObjectNotFound as e:
        raise HTTPNotFound(
            title=f"Aucun {model.__class__.__name__} trouvé avec l'id {id}"
        )
    except orm.OperationWithDeletedObjectError as e:
        raise HTTPNotFound(
            title=f"Aucun {model.__class__.__name__} trouvé avec l'id {id}"
        )

    return item


class NameMixin:
    @classproperty
    def name(self) -> str:
        """nom du modèle"""
        return self.__name__

    @classproperty
    def url_name(self) -> str:
        """url du modèle
        add s ou x sauf si déjà s ou x """
        return (
            self.__name__.lower()
            if self.__name__[-1] in ["s", "x"]
            else self.__name__.lower() + "s"
        )


class SetMixin:
    def set(self, **kwargs: dict):
        """
        Override default set pour vérifier si updatable

        Args:
            kwargs: field : nouvelle valeur

        Raises:
            AttributeError: si le field n'est pas dans :attr:`updatable`.
        """
        for item in kwargs:
            if item not in self.updatable:
                raise AttributeError(f"{item} n'est pas updatable")

        super().set(**kwargs)


class CapWordsMixin:
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
