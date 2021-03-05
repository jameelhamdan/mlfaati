import shortuuid
from baseconv import BASE62_ALPHABET, base62
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _


ShortUUID = shortuuid.ShortUUID(alphabet=BASE62_ALPHABET)


def int_to_str(number) -> str:
    return base62.encode(number)


def str_to_int(value) -> int:
    return int(base62.decode(value))


class AutoUUIDField(models.Field):
    """
    An auto short UUID field that uses base62 to convert str uuid to int to store in db
    """

    default_error_messages = {
        'invalid': _("'%(value)s' is not a valid ID."),
    }
    empty_strings_allowed = False

    def get_default(self):
        """Return the default value for this field."""
        # TODO: Improve this function to return a more unique value that's 10 char long
        return shortuuid.random(10)

    def __init__(self, auto=True, *args, **kwargs):
        self.auto = auto
        kwargs['editable'] = False
        kwargs['blank'] = False
        kwargs['unique'] = True
        kwargs['primary_key'] = True
        kwargs['db_index'] = True
        super(AutoUUIDField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return None

    def get_internal_type(self):
        return 'BigIntegerField'

    def rel_db_type(self, connection):
        return self.db_type(connection)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if not isinstance(value, str):
            value = self.to_python(value)
        return str_to_int(value)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is not None and not isinstance(value, str):
            try:
                if isinstance(value, int):
                    return int_to_str(value)
                raise ValueError
            except (AttributeError, ValueError):
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return value
