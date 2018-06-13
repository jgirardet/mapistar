from pony import orm
from .base_db import db
from apistar import http


class Document(db.Entity):
    name = orm.Optional(str)
    file = orm.Optional(str)
    title = orm.Optional(str)
    content_type = orm.Optional(str)
    correspondance = orm.Required("Acte")


def send_document(data: http.RequestData):
    if isinstance(data, dict):
        data = {
            key: value
            if not hasattr(value, "filename")
            else {"filename": value.filename, "content": value.read().decode("utf-8")}
            for key, value in data.items()
        }
    return {"data": data}
