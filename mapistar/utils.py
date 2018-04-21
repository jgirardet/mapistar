# Standard Libraries
import importlib

# Third Party Libraries
import pendulum


def import_models(module_liste: list):
    """
    Import tous les modules contenant des Entity ponyorm

    Doit être appelé avant le db.bind()
    """
    for i in module_liste:
        importlib.import_module("mapistar." + i)


class PendulumDateTime:
    """ Helper Descriptor for datetime

    Utile pour utiliser les datetime non aware et les utliser en aware.

    Usage::
        class Test:
            _created = orm.Required(datetime)
            created = PendulumDateTime()

    Les 2 fields ne doivent différer que par le "_".

    le _field ne doit pas être accéder directement.
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
