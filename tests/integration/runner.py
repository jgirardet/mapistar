from pony.orm import db_session, flush

from tests.factory import medicamentf, observationf, ordonnancef, patientf, userf


def many(nombre, factory, **kwargs):
    """range qui commence à 1 au lieu de 0"""
    for i in range(1, nombre + 1):
        factory(**kwargs)


@db_session
def generate_db():
    j = userf(username="j")
    userf(username="k")
    l = userf(username="l")
    flush()
    j.permissions.del_patient = True
    l.is_admin = True
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
    many(3, ordonnancef, patient=2, owner=1)  # 19-20-21
    flush()
    many(3, medicamentf, ordonnance=17)  # 1-2-3
    many(3, medicamentf, ordonnance=18)  # 4-5-6
    many(3, medicamentf, ordonnance=19)  # 7-8-9
    flush()
