from mapistar.actes.actes import ActeCreateSchema
from mapistar.actes.observations import (
    Observation,
    ObservationCreateSchema,
    ObservationUpdateSchema,
)
from mapistar.actes.ordo_items import (
    ItemCreateSchema,
    Medicament,
    MedicamentCreateSchema,
    MedicamentUpdateSchema,
)
from mapistar.actes.ordonnances import (
    Ordonnance,
    OrdonnanceCreateSchema,
    OrdonnanceUpdateSchema,
)
from mapistar.actes.schemas import actes_schemas


def test_acte():
    assert "patient" in ActeCreateSchema.validator.required


def test_actes_schemas():
    assert len(actes_schemas) == 2


def test_observation():
    assert issubclass(ObservationCreateSchema, ActeCreateSchema)
    assert "motif" in ObservationCreateSchema.validator.required
    assert (
        set(Observation.updatable)
        == set(ObservationUpdateSchema.validator.properties.keys())
    )


def test_ordonnance():
    assert issubclass(OrdonnanceCreateSchema, ActeCreateSchema)
    assert (
        set(Ordonnance.updatable)
        == set(OrdonnanceUpdateSchema.validator.properties.keys())
    )


def test_medicament():
    assert issubclass(MedicamentCreateSchema, ItemCreateSchema)
    assert {"cip", "nom"}.issubset(set(MedicamentCreateSchema.validator.required))
    assert (
        set(Medicament.updatable)
        == set(MedicamentUpdateSchema.validator.properties.keys())
    )
