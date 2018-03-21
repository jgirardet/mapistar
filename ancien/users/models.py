# Standard Libraries
import typing

STATUT = ['docteur', 'secrétaire', 'interne', 'remplaçant']

from mapistar.models import db
from pony import orm

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Entity):
    """
    Base User class for unolog
    define statu
    """
    pk = orm.PrimaryKey(int, auto=True)
    username = orm.Required(str)
    password = orm.Required(str)

    def __repr__(self):
        """
        nice printing Firstname Name
        """
        return f"[User: {self.username}]"

    @staticmethod
    def _set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    @orm.db_session
    def create_user(cls, username, password):
        pwd = cls._set_password(password)
        user = db.User(username=username, password=pwd)
        user.flush()
        return user

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


"""
RPPS
ADELI


https://github.com/codingforentrepreneurs/srvup-rest-framework/blob/master/src/accounts/models.py
"""
