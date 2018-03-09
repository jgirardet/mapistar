# Standard Libraries
import typing

# Third Party Libraries
from apistar import typesystem

# yapf: disable


"""
Base class for various schemas type

Be carrefull, each pattern should be 0 or many to not fail if empty

"""


# yapf: disable
class RegularText(typesystem.String):
    """
    standard text
    """

    errors = typesystem.String.errors.copy()
    errors['pattern'] = "Seuls les lettres, - et espace sont des charactères valides"
    pattern = r"^[a-zA-ZáàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ -]*$"
    description = "a charfield"


class FormattedDate(typesystem.String):
    """
    date formated yyyy-mm-dd
    """
    pattern = r"^([0-9]{4})(-)?(1[0-2]|0[1-9])(?(2)-)(3[0-1]|0[1-9]|[1-2][0-9])$"
    errors = typesystem.String.errors.copy()
    errors['pattern'] = "The following format should be used : yyyy-mm-dd"
    description = "Date formated yyyy-mm-dd"


class EmailSchema(typesystem.String):
    """
    Email
    """
    pattern = r"^([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)?$"
    errors = typesystem.String.errors.copy()
    errors['pattern'] = "Please enter a valid e-mail adress"
    description = "Email"


def regular_text(**kwargs) -> typing.Type:
    return type('RegularText', (RegularText, ), kwargs)


def formatted_date(**kwargs) -> typing.Type:
    return type('FormattedDate', (FormattedDate, ), kwargs)


def email_schema(**kwargs) -> typing.Type:
    return type('EmailSchema', (EmailSchema, ), kwargs)
