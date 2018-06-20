import pytest

from mapistar.documents import (
    get_new_path,
    get_new_filename,
    get_new_directory,
    post_document,
)
import pathlib
from simple_settings import settings
from apistar import exceptions
import io


def test_get_new_filename():
    a = get_new_filename("application/pdf").split(".")
    assert len(a[0]) == 32
    assert a[1] == "pdf"


def test_get_new_directory():
    a = get_new_directory("a1grergerg")
    assert str(a) == "a/1"


def test_new_path(mocker):
    mocker.patch.object(settings, "STATIC_DIR", "/bla/ble")
    print(settings.STATIC_DIR)
    a = get_new_path("318ed983dcc443738c8788d249822189.pdf")
    assert str(a) == "/bla/ble/3/1/318ed983dcc443738c8788d249822189.pdf"


def test_post_document_fail(mdocu, mocker):

    mocker.patch("mapistar.documents.get_or_404")

    m = mocker.MagicMock()

    del m.filename
    with pytest.raises(exceptions.BadRequest) as exc:
        post_document(1, data={1: m})
    assert str(exc.value) == "un fichier doit être envoyé"

    m.filename = "mkook.exe"
    with pytest.raises(exceptions.BadRequest) as exc:
        post_document(1, data={1: m})
    assert str(exc.value)[:20] == "Extension autorisées"


@pytest.mark.pony
def test_post_doc_succceeds(acte, tmpdir, mocker):
    mocker.patch.object(settings, "STATIC_DIR", tmpdir)
    print(settings.STATIC_DIR)
    m = io.BytesIO(b"blabla")
    m.filename = "oladdd.pdf"
    r = post_document(acte.id, data={1: m})
    assert r[0]["id"] == 1

    r = post_document(acte.id, data={1: m, 2: m, 3: m})
    assert {x["id"] for x in r} == {2, 3, 4}
    assert 4 == len(list(tmpdir.visit(fil="*.pdf")))
