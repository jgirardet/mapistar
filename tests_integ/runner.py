from tests.factory import patientf, userf, observationf, ordonnancef, medicamentf

from pony.orm import db_session, flush


def many(nombre, factory, **kwargs):
    """range qui commence à 1 au lieu de 0"""
    for i in range(1, nombre + 1):
        factory(**kwargs)


@db_session
def generate_db():
    userf(username="j")
    userf(username="k")
    flush()
    many(8, patientf)
    flush()
    many(3, observationf, patient=1, owner=1)
    many(3, observationf, patient=1, owner=2)
    many(3, observationf, patient=2, owner=1)
    many(3, observationf, patient=2, owner=2)
    flush()
    many(3, ordonnancef, patient=1, owner=1)  # 13-14-15
    many(3, ordonnancef, patient=1, owner=2)  # 16-17-18
    flush()
    many(3, medicamentf, ordonnance=17)
