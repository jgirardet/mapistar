import pytest

from mapistar.documents import validate, Document, routes_documents
import pathlib
from simple_settings import settings
from apistar import exceptions
import io

from unittest.mock import MagicMock, patch

D = MagicMock(spec=Document)


class TestDocument:
    def test_get_new_filename(self):
        a = str(Document.get_new_filename("application/pdf")).split(".")
        assert len(a[0]) == 32
        assert a[1] == "pdf"

    def test_directory(self, mocker):
        a = Document.directory.fget(mocker.MagicMock(**{"filename": "a1ergergerg"}))
        assert str(a) == "a/1"

    def test_new_path(self, mocker):
        mocker.patch.object(settings, "DOCUMENTS_DIR", "/bla/ble")
        a = Document.path.fget(
            mocker.MagicMock(
                **{
                    "directory": "3/1",
                    "filename": "318ed983dcc443738c8788d249822189.pdf",
                }
            )
        )
        assert str(a) == "/bla/ble/3/1/318ed983dcc443738c8788d249822189.pdf"

    def test_write_erase(self, tmpdir):
        a = MagicMock(**{"path": pathlib.Path(tmpdir, "heelo.txt")})
        Document.write(a, io.BytesIO(b"hello"))
        assert tmpdir.join("heelo.txt") in tmpdir.listdir()
        Document.erase(a)
        assert tmpdir.join("heelo.txt") not in tmpdir.listdir()

    def test_load(self, tmpdir, mocker):
        a = pathlib.Path(tmpdir, "load.txt")
        a.write_bytes(b"123")
        m = mocker.MagicMock(**{"path": a})
        a = Document.content.fget(m)
        assert a == b"123"

    def test_dico(self, mocker):
        m = mocker.MagicMock(**{"url": "/bla/1/"})
        with patch("builtins.super") as n:
            n.return_value.dico = {}
            d = Document.dico.fget(m)
        assert d["url"] == "/bla/1/"

    def test_url(self, mocker):
        link = None
        for r in routes_documents.routes:
            if r.name == "one":
                link = r.link.url
        m = mocker.MagicMock(**{"id": 3})
        assert link.format(document_id=3) == Document.url.fget(m)


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

    # tester validate success


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
#     assert r.content["success"][0]["id"] == 1

# r = post_document(acte.id, data={1: n, 2: o, 3: p})
# assert {x["id"] for x in r} == {2, 3, 4}
# assert 2 == len(list(arbo.visit(fil="*.pdf")))
# assert 4 == len(list(arbo.visit(fil="*.*")))
# assert {"pdf", "jpg", "zip"} == {
#     str(e).split(".")[-1] for e in arbo.visit(fil="*.*")
# }
