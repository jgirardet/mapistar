# Standard Libraries
import importlib
from datetime import date, datetime

# Third Party Libraries
from apistar.exceptions import NotFound
from descriptors import classproperty
from pony import orm

# mapistar
from mapistar.exceptions import MapistarProgrammingError


def check_config(settings):

    # checl jwt_duration
    if not settings.JWT_DURATION:  # pragma: no cover
        raise MapistarProgrammingError("La durée des JWT doit être précisée")


def import_models(module_liste: list):
    """
    Import tous les modules contenant des Entity ponyorm

    Doit être appelé avant le db.bind()

    Args:
        module_liste: Liste des moduels où se trouvent les Entities Pony.
    """
    for item in module_liste:
        if isinstance(item, str):
            importlib.import_module(".".join(("mapistar", item)))
        elif isinstance(item, tuple):
            for module in item[1]:
                importlib.import_module(".".join(("mapistar", item[0], module)))
        else:
            raise MapistarProgrammingError(
                "Déclaration de module sous la forme str ou tuple('base', ('module1','modele2'))"
            )


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
        raise NotFound

    return item


class DicoMixin:
    @property
    def dico(self) -> dict:
        """
        Transforme un dict en dict serializable.

        Marche pour:
            *object datetime
            *object date

        Args:
            dico: le dict à transformer
        Returns:
            un nouveau dict.
        """
        new_dict = {}

        for k, v in self.to_dict().items():
            if isinstance(v, datetime):
                new_dict[k] = v.isoformat()

            elif isinstance(v, date):
                new_dict[k] = v.isoformat()
            else:
                new_dict[k] = v
        return new_dict


class NameMixin:
    @classproperty
    def name(self) -> str:
        """nom du modèle"""
        return self.__name__

    @classproperty
    def url_name(self) -> str:
        """url du modèle"""
        return self.__name__.lower() + "s"


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
