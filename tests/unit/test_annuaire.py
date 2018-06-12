import pytest

from mapistar.annuaire import Praticien

entry = [
    "8",
    "10002727377",
    "810002727377",
    "DR",
    "Docteur",
    "ORTEGA",
    "JOSE",
    "10",
    "Médecin",
    "C",
    "Civil",
    "SM53",
    "Spécialiste en Médecine Générale",
    "S",
    "Spécialité ordinale",
    "",
    "",
    "",
    "",
    "CABINET DU DR JOSE ORTEGA",
    "CABINET DU DR JOSE ORTEGA",
    "410002727377008",
    "",
    "",
    "",
    "",
    "",
    "",
    "ROUTE DE GRASSAC",
    "",
    "16380 MARTHON",
    "16380",
    "16211",
    "Marthon",
    "99000",
    "France",
    "",
    "",
    "",
    "",
    "ortega.jose377@sephira.mssante.fr",
    "",
]


class TestModelPraticien:
    def test_capsword_is_called(self, mocker):
        a = mocker.MagicMock(spec=Praticien)
        Praticien.before_update(a)
        a._capwords.assert_called()

    @pytest.mark.pony
    def test_from_annuaire(self):
        a = Praticien.from_annuaire(entry)
        assert a.to_dict() == {
            "id": 1,
            "civilite": "Docteur",
            "nom": "Ortega",
            "prenom": "Jose",
            "rpps": "10002727377",
            "rue": "ROUTE DE GRASSAC",
            "cp": "16380",
            "ville": "10002727377",
            "tel": "",
            "portable": "",
            "email": "",
            "mssante": "ortega.jose377@sephira.mssante.fr",
            "profession": "Médecin",
            "specialite": "Spécialiste en Médecine Générale",
        }
        assert len(a.to_dict()) == 14
