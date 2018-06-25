import uuid

import mimetypes
from apistar import Include, Route, exceptions, http
from apistar.http import JSONResponse
from mapistar.exceptions import MapistarProgrammingError, MapistarInternalError
from mapistar.utils import get_or_404
from pathlib import Path
from pony import orm
from simple_settings import settings

from .base_db import db
from mapistar.utils import DicoMixin

AUTHORIZED_CONTENT_TYPE = (
    "application/pdf",
    "application/zip",
    "audio/basic",
    "audio/mpeg",
    "audio/x-wav",
    "image/gif",
    "image/jpeg",
    "image/png",
    "text/csv",
    "text/html",
    "text/plain",
    "text/richtext",
    "text/x-vcard",
    "video/mp4",
    "video/mpeg",
)


class Document(DicoMixin, db.Entity):
    filename = orm.Required(str)
    content_type = orm.Optional(str)
    acte = orm.Required("Acte")

    @property
    def directory(self):
        """subdirectory given the filename"""
        return Path(*self.filename[:2])

    @property
    def path(self):
        """absolute path of the file"""
        return Path(settings.DOCUMENTS_DIR, self.directory, self.filename)

    def write(self, file):
        """write file to disk"""
        self.path.write_bytes(file.read())

    def erase(self):
        """delete file from disk"""
        self.path.unlink()

    @staticmethod
    def get_new_filename(content_type):
        """giver a content type, return a uuencoded name with right extension"""
        ext = mimetypes.guess_extension(content_type)
        # jpeg sometimes return jpe
        ext = ".jpg" if ext == ".jpe" else ext
        return Path(uuid.uuid4().hex + ext)

    def load(self):
        return self.path.read_bytes()

    @classmethod
    def new(cls, old_filename, content_type, stream, acte):
        """ ajoute un nouveau fichier dans la bae de donnée et sur le disk"""
        d = Document(
            filename=str(cls.get_new_filename(content_type)),
            content_type=content_type,
            acte=acte,
        )

        try:
            d.write(stream)
        except Exception as exc:
            d.delete()
            return

        return d


def validate(data):
    """
    Validate multipart content.

    Return
        validated_files(dict)

    """

    validated_files = []
    for key, value in data.items():
        if not hasattr(value, "filename"):
            raise exceptions.BadRequest("un fichier doit être envoyé")

        content_type = mimetypes.guess_type(value.filename)[0]
        if content_type not in AUTHORIZED_CONTENT_TYPE:
            raise exceptions.BadRequest(
                f"Extension autorisées : {AUTHORIZED_CONTENT_TYPE}"
            )

        validated_files.append(
            {"content_type": content_type, "content": value, "filename": value.filename}
        )

    return validated_files


def post(acte_id: int, data: http.RequestData) -> http.JSONResponse:

    """
    Ajouter un ou des nouveaux documents à un Acte

    Returns:
        200 : tout ok
        500 : rien ok
        207 : 200: contenu ok, 500: message d'erreurs
    """

    acte = get_or_404(db.Acte, acte_id)

    entities = []
    errors = []
    vf = validate(data)

    for f in vf:
        d = Document.new(
            old_filename=f["filename"],
            content_type=f["content_type"],
            stream=f["content"],
            acte=acte,
        )
        if d:
            entities.append(d)
        else:
            errors.append(f"Une erreur s'est produite avec {f['filename']}")

    if entities and not errors:
        return http.JSONResponse([e.to_dict() for e in entities], 201)
    elif entities and errors:
        return http.JSONResponse(
            {200: [e.to_dict() for e in entities], 500: [e for e in errors]}, 207
        )
    else:
        return http.JSONResponse([e for e in errors], 500)


from mapistar.permissions import ActesPermissions
from apistar import App


def delete(document_id: int, obj: ActesPermissions) -> dict:
    """
    Supprime un documents
    """
    try:
        obj.erase()
    except Exception as exc:
        print(exc)
        raise MapistarInternalError(str(exc))

    obj.delete()
    return {"id": document_id, "deleted": True}


def one(document_id: int, app: App) -> http.Response:
    """
    one document
    """
    doc = get_or_404(db.Document, document_id)
    return http.Response(
        doc.load(),
        headers={
            "content-type": doc.content_type,
            "Cache-Control": "no-cache, no-store, must-revalidate",
        },
    )


routes_documents = Include(
    url="/documents",
    name="documents",
    routes=[
        Route(url="/{acte_id}/", method="POST", handler=post),
        # Route(url="/", method="GET", handler=liste),
        # Route(url="/{patient_id}/", method="PUT", handler=update),
        Route(url="/{document_id}/", method="DELETE", handler=delete),
        Route(url="/{document_id}/", method="GET", handler=one),
    ],
)
