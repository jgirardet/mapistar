# Third Party Libraries
import falcon
import hug
import pendulum

from mapistar import directives

# mapistar
from mapistar.base_db import db
from mapistar.exceptions import MapistarForbidden
from mapistar import get_or_404
from pony import orm
from typing import Union
from werkzeug.security import check_password_hash, generate_password_hash


# from mapistar.main import jwtoken


@hug.post("/login")
def login(hug_jwt, username: hug.types.text, password: hug.types.text):
    """
    View d'authentification

    Args:
        credentials: credentials username/password
        jwt: JWT componement pour l'encodage du payload

    Toutes les erreurs "raise"

    Returns:
        token
    """
    user = db.User.get(username=username)

    if not user or not user.check_password(password):
        raise falcon.HTTPForbidden(title="Incorrect username or password.")

    if not user.actif:
        raise falcon.HTTPForbidden(title="Utilisateur inactif")

    payload = {
        "id": user.id,
        "username": user.username,
        "iat": pendulum.now(),
        "exp": pendulum.now() + pendulum.Duration(seconds=1000),
    }
    token = hug_jwt.encode(payload)
    if token is None:
        raise falcon.HTTPServiceUnavailable(title="échec de l'encodage jwt")

    return token


# from marshmallow import Schema, fields


# class ChangePaswordSchema(Schema):
#     old = fields.Str()
#     new1 = fields.Str()
#     new2 = fields.Str()


# @hug.post("")
# def change_password(pwd: hug.types.MarshmallowSchema(ChangePaswordSchema()), hug_user):
#     """
#     Update users password
#     """
#     # user = get_or_404(User, user.id)
#     hug_user.change_password(**pwd)
#     return {"msg": "password changed"}


# def get_new_password(user: JWTUser) -> dict:
#     user = get_or_404(User, user.id)
#     return {"password": user.get_new_password()}


# class NewUserSchema(types.Type):
#     username = validators.String()
#     password = validators.String()
#     nom = validators.String()
#     prenom = validators.String()
#     statut = validators.String(enum=STATUT)
#     actif = validators.Boolean(default=False)


# def create_user(
#     data: NewUserSchema, user: User
# ) -> Union[http.JSONResponse, http.HTMLResponse]:
#     """ajouter un nouvel utilisateur"""

#     if user.is_admin:
#         user = db.User.create_user(**data)
#         return http.JSONResponse(user.to_dict(), status_code=201)
#     else:
#         raise MapistarForbidden("Seul un admin peut ajouter un utilisateur")


# routes_users = Include(
#     url="/users",
#     name="users",
#     routes=[
#         Route(url="/login/", method="POST", handler=login, name="login"),
#         Route(url="/change_password/", method="POST", handler=change_password),
#         Route(url="/get_new_password/", method="GET", handler=get_new_password),
#         # Route(url="/{id}/", method="PUT", handler=update),
#         # # Route(url="/patients/", method="DELETE", handler=delete),
#         # Route(url="/{id}/", method="DELETE", handler=delete),
#         Route(url="/create_user/", method="POST", handler=create_user),
#     ],
# )

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
