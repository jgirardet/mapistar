# Standard Libraries
import inspect
import re

# Third Party Libraries
import cerberus
from apistar.server.validation import ValidatedRequestData
from apistar import Component, exceptions


def date_validator(field, value, error):
    if not re.match(r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$',
                    value):
        error(field, "Must be parsable date")
