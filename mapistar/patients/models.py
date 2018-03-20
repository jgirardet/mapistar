from pony.orm import Required, Optional

from datetime import date

from mapistar.base_db import db
from string import capwords


class Patient(db.Entity):
    nom = Required(str)
    prenom = Required(str)
    ddn = Required(date)
    rue = Optional(str, 200)
    postalcode = Optional(int)
    city = Optional(
        str,
        200,
    )
    phonenumber = Optional(int)
    email = Optional(str, 100)

    # alive = Optional(bool, default=True)

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
