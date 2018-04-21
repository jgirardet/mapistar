# Third Party Libraries
import importlib
import pendulum
from apistar.exceptions import NotFound
from pony import orm


def import_models(module_liste: list):
    """
    Import tous les modules contenant des Entity ponyorm

    Doit être appelé avant le db.bind()

    Args:
        module_liste: Liste des moduels où se trouvent les Entities Pony.
    """
    for i in module_liste:
        importlib.import_module("mapistar." + i)


class PendulumDateTime:
    """
    Helper Descriptor for datetime

    Utile pour utiliser les datetime non aware et les utliser en aware.

    Example::

        class Test:
            _created = orm.Required(datetime)
            created = PendulumDateTime(

    Les 2 fields ne doivent différer que par le "_".

    le field "_" ne doit pas être accédé directement.

    Returns:
        Pour le get c'est un objet :class:`pendulum.DateTime` en UTC.
    """

    def __set_name__(self, owner, name):
        self.field = "_" + name

    def __get__(self, instance, owner) -> pendulum.DateTime:
        """
        Convertit naif datetime  en aware.
        On ajoute le in_tz('UTC') pour s'assurer que l'objet ne reste pas unaware
        """
        return pendulum.instance(getattr(instance, self.field)).in_tz("UTC")

    def __set__(self, instance, value):
        """
        Convertit aware en naif. Tout est sauvé en UTC
        """
        setattr(instance, self.field, value.in_tz("UTC").naive())


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
