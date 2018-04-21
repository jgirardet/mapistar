class MapistarException(Exception):
    """
    Base Mapistar Exception
    """


class MapistarProgrammingError(MapistarException):
    """
    Raised en cas de mauvaise configuration du code.
    Equivalent d'un assert
    """
