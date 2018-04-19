import importlib
from apistar import exceptions


def check_actes_alter_permission(obj, user_id):
    """
    Permissions pour update et delete
    """

    # if obj.created.date() != timezone.now().date():
    #     raise BadRequest("Observation can't be edited another day")

    if obj.owner != obj.owner:
        raise exceptions.Forbidden(
            "Un utilisateur ne peut modifier un acte créé par un autre utilisateur"
        )


def import_models(module_liste: list):
    """
    Import tous les modules contenant des Entity ponyorm

    Doit être appelé avant le db.bind()
    """
    for i in module_liste:
        importlib.import_module("mapistar." + i)
