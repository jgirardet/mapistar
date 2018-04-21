# Standard Libraries
from datetime import date
from string import capwords

# Third Party Libraries
from pony.orm import Optional, PrimaryKey, Required

# mapistar
from mapistar.base_db import db


class Patient(db.Entity):
    pk = PrimaryKey(int, auto=True)
    nom = Required(str)
    prenom = Required(str)
    ddn = Required(date)
    # sexe = Optional(bool)
    rue = Optional(str, 200)

    # postalcode = Optional(int)
    # city = Optional(
    #     str,
    #     200,
    # )
    # phonenumber = Optional(int)
    # email = Optional(str, 100)

    # # alive = Optional(bool, default=True)

    def __repr__(self):
        """
        nice printing Firstname Name
        """
        return f"[Patient: {self.prenom} {self.nom}]"

    def _capwords(self):

        self.nom = capwords(self.nom)
        self.prenom = capwords(self.prenom)

    def before_insert(self):
        self._capwords()

    def before_update(self):
        self._capwords()


"""
champs à ajouter :
date de décès
décédé
médecin traitant déclaré
notes divers
"""
