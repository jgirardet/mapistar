from pony import orm
from .base_db import db
from apistar import http, exceptions
from simple_settings import settings
import mimetypes
import uuid
from mapistar.utils import get_or_404


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


def send_document(acte_id: int, data: http.RequestData):
    acte = get_or_404(db.Acte, acte_id)

    files = []
    for key, value in data.items():
        if not hasattr(value, "filename"):
            raise exceptions.BadRequest("un fichier doit être envoyé")

        content_type = mimetypes.guess_type(value.filename)
        if content_type not in AUTHORIZED_CONTENT_TYPE:
            raise exceptions.BadRequest(
                f"Extension autorisées : {AUTHORIZED_CONTENT_TYPE}"
            )

        new_filename = get_new_filename(content_type)

        with open(new_filename, "wb") as f:
            f.write(value.read())

        d = Document(filename=new_filename, content_type=content_type, acte=acte)
        d.flush()

        files.append({"content_type": content_type, "content": value.read()})

    return {"data": data}
