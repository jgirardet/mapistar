from apistar import validators

# class Email(String):
#     def __init__(self, **kwargs):
#         super().__init__(pattern=)
# class DateTime(String):
#     def __init__(self, **kwargs):
# super().__init__(format='datetime', **kwargs)
import re
email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$',
    re.IGNORECASE)  # domain

# a = re.search(email_re, "zef@fzef.gftr")
# print(a)


class Email(validators.String):
    def __init__(self, **kwargs):
        super().__init__(pattern=email_re, **kwargs)


assert pattern is None or isinstance(pattern, str) or isinstance(
    pattern, re._pattern_type)  #type(re.compile('')))
# or isinstance(
#            pattern, re._pattern_type

# email = Email()
# email.validate("mokm")

# a = validators.String(pattern=email_re)

a = Email()
print(a.validate("dazfze@ze.gt"))
