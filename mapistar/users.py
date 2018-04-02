# Standard Libraries
import typing

# Third Party Libraries
from pony import orm
from werkzeug.security import check_password_hash, generate_password_hash

# mapistar
from mapistar.models import db

STATUT = ['docteur', 'secrétaire', 'interne', 'remplaçant']


class User(db.Entity):
    """
    Base User class for unolog
    define statu
    """
    pk = orm.PrimaryKey(int, auto=True)
    username = orm.Required(str, unique=True)
    password = orm.Required(str)
    nom = orm.Required(str)
    prenom = orm.Required(str)
    actes = orm.Set('Acte')

    def __repr__(self):
        """
        nice printing Firstname Name
        """
        return f"[User: {self.prenom} {self.nom}]"

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def create_user(cls, username, password, nom, prenom):
        pwd = generate_password_hash(password)
        user = db.User(username=username, password=pwd, nom=nom, prenom=prenom)
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

"""
