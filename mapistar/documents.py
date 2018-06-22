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
    ext = mimetypes.guess_extension(content_type)
    # jpeg sometimes return jpe
    ext = ".jpg" if ext == ".jpe" else ext
    return uuid.uuid4().hex + ext


def get_new_directory(filename):
    return Path(*filename[:2])


def get_new_path(filename):
    return Path(settings.STATIC_DIR, get_new_directory(filename), filename)


# def save_document(path):

#     some_files  = [...]

#     new_entity =[]

#     for file in some_files:
#         try:
#             d  = Document(*args)
#             d.flush()
#             savefile
#         except orm.OrmError:
#             raise someother error
#         except IOError:
#             rollback
#             raise someerror
#         else:
#             new_entity .append(d)

#     return new_entity


# def save_file(filename, saved_files, ...):
#     <do save>
#     saved_files.append(filename)

# def save_document(path):
#     files_to_save = [...]
#     saved_files = []
#     new_entities = []

#     try:
#         with db_session:
#             for file in files_to_save:
#                 d = Document(*args)
#                 new_entities.append(d)
#                 d.flush()
#                 save_file(file, saved_files, ...)
#     except:
#         for filename in saved_files:
#             remove_file(filename)
#         raise
#     return new_entities


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
            {
                "filename": value.filename,
                "content_type": content_type,
                "content": value,
                "new_filename": get_new_filename(content_type),
            }
        )

    return validated_files


def save_files(files):
    pass


def post_document(acte_id: int, data: http.RequestData):
    pass


#     """
#     Ajouter un nouveau document à un Acte
#     """
#     acte = get_or_404(db.Acte, acte_id)

#     entites = []
#     files = []

#     vf = validate(data)

#     d = Document(filename=new_filename, content_type=content_type, acte=acte)

#     p = get_new_path(new_filename)
#     p.write_bytes(value.read())

#     files.append(d)

#     return [doc.to_dict() for doc in files]
