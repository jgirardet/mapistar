# Third Party Libraries
from apistar import exceptions


class MapistarException(Exception):
    """
    Base Mapistar Exception
    """


class MapistarHttpException(exceptions.HTTPException):
    """
    base HTtp Eexceptoin
    """


class MapistarProgrammingError(MapistarException):
    """
    Raised en cas de mauvaise configuration du code.
    Equivalent d'un assert
    """


class MapistarBadRequest(MapistarException, exceptions.BadRequest):
    """
    Raised en cas de mauvaise configuration du code.
    Equivalent d'un assert
    """
