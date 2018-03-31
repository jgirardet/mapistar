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


class MapistarValidator(cerberus.Validator):
    @property
    def __name__(self):
        return repr(self)

    def validate(self, *args, **kwargs):
        kwargs['update'] = self._config.get("update", False)
        super().validate(*args, **kwargs)


class CerberusComp(Component):
    def can_handle_parameter(self, parameter: inspect.Parameter):
        return isinstance(parameter.annotation, cerberus.Validator)

    def resolve(self, parameter: inspect.Parameter,
                data: ValidatedRequestData):

        v = parameter.annotation
        validated_data = v.validated(data)
        if validated_data:
            return validated_data
        else:
            raise exceptions.BadRequest(v.errors)
