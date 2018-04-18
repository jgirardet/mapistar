# Standard Libraries
import re

# Third Party Libraries

import importlib


def date_validator(field, value, error):
    if not re.match(r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$", value):
        error(field, "Must be parsable date")


# from mapistar.users import User

# class MapistarUserComponent:
#     def on_request(self,


# def check_actes_alter_permission(obj, user_id):
#     """
#     Permissions pour update et delete
#     """

#     if obj.created.date() != timezone.now().date():
#         raise BadRequest("Observation can't be edited another day")

#     if auth.user != obj.owner:
#         raise Forbidden("Only owner can edit an Observation")


def import_models(module_liste: list):
    """
    Import tous les modules contenant des Entity ponyorm

    Doit être appelé avant le db.bind()
    """
    for i in module_liste:
        importlib.import_module("mapistar." + i)
