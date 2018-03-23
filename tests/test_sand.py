from apistar import types, validators

from mapistar.patients import PatientSchema


def test_sand():
    a = PatientSchema(
        nom='mok', prenom='okmok', ddn='1234-12-12', sexe='f', bla='')