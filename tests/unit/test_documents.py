import pytest

from mapistar.documents import (
    get_new_path,
    get_new_filename,
    get_new_directory,
    post_document,
    validate,
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


def test_validate(mdocu, mocker):

    m = mocker.MagicMock()

    del m.filename
    with pytest.raises(exceptions.BadRequest) as exc:
        validate(data={1: m})
    assert str(exc.value) == "un fichier doit être envoyé"

    m.filename = "mkook.exe"
    with pytest.raises(exceptions.BadRequest) as exc:
        validate(data={1: m})
    assert str(exc.value)[:20] == "Extension autorisées"


# @pytest.mark.pony
# def test_post_doc_succceeds(acte, arbo, mocker):
#     mocker.patch.object(settings, "STATIC_DIR", arbo)

#     m = io.BytesIO(b"blabla")
#     n = io.BytesIO(b"blabla")
#     o = io.BytesIO(b"blabla")
#     p = io.BytesIO(b"blabla")
#     m.filename = "a.pdf"
#     n.filename = "b.pdf"
#     o.filename = "e.jpg"
#     p.filename = "f.zip"
#     r = post_document(acte.id, data={1: m})
#     assert r[0]["id"] == 1

#     r = post_document(acte.id, data={1: n, 2: o, 3: p})
#     assert {x["id"] for x in r} == {2, 3, 4}
#     assert 2 == len(list(arbo.visit(fil="*.pdf")))
#     assert 4 == len(list(arbo.visit(fil="*.*")))
#     assert {"pdf", "jpg", "zip"} == {
#         str(e).split(".")[-1] for e in arbo.visit(fil="*.*")
#     }
