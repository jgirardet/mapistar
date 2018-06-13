import pytest

from mapistar.documents import Document, get_new_filename, send_document
import pathlib
from simple_settings import settings
from apistar import exceptions


def test_get_new_filename():
    a = get_new_filename("application/pdf").split(".")
    assert len(a[0]) == 32
    assert a[1] == "pdf"


def test_send_document(mdocu, mocker):

    mocker.patch("mapistar.documents.get_or_404")

    m = mocker.MagicMock()

    del m.filename
    with pytest.raises(exceptions.BadRequest) as exc:
        send_document(1, data={1: m})
    assert str(exc.value) == "un fichier doit être envoyé"

    m.filename = "mkook.exe"
    with pytest.raises(exceptions.BadRequest) as exc:
        send_document(1, data={1: m})
    assert str(exc.value)[:20] == "Extension autorisées"
