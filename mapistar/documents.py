from pony import orm
from .base_db import db
from apistar import http, exceptions
from simple_settings import settings
import mimetypes
import uuid
from mapistar.utils import get_or_404
from pathlib import Path

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


class Document(db.Entity):
    filename = orm.Required(str)
    content_type = orm.Optional(str)
    acte = orm.Required("Acte")


def get_new_filename(content_type):
    return uuid.uuid4().hex + mimetypes.guess_extension(content_type)


def get_new_directory(filename):
    return Path(*filename[:2])


def get_new_path(filename):
    return Path(settings.STATIC_DIR, get_new_directory(filename), filename)


def post_document(acte_id: int, data: http.RequestData):
    acte = get_or_404(db.Acte, acte_id)

    files = []
    for key, value in data.items():
        if not hasattr(value, "filename"):
            raise exceptions.BadRequest("un fichier doit être envoyé")

        content_type = mimetypes.guess_type(value.filename)[0]
        if content_type not in AUTHORIZED_CONTENT_TYPE:
            raise exceptions.BadRequest(
                f"Extension autorisées : {AUTHORIZED_CONTENT_TYPE}"
            )

        new_filename = get_new_filename(content_type)

        p = Path(get_new_path(new_filename))
        p.write_bytes(value.read())

        d = Document(filename=new_filename, content_type=content_type, acte=acte)
        files.append(d)

    return [doc.to_dict() for doc in files]
