from pony import orm


class Document(orm.Entity):
    name = orm.String()
    file = orm.String()
