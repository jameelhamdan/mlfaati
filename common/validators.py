import re

from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


AlphaValidator = RegexValidator(r'^[a-zA-Z ]*$', _('Only english characters are allowed.'))


@deconstructible
class SpaceNameValidator(RegexValidator):
    regex = r'^[a-z0-9_+@-]+$'
    message = _(
        'Enter a valid space name. This value may contain only lower case english letters, '
        'numbers, and @/+/-/_ characters.'
    )
    flags = re.ASCII


@deconstructible
class PipelineNameValidator(RegexValidator):
    regex = r'^[a-z0-9_+@-]+$'
    message = _(
        'Enter a valid pipeline name. This value may contain only lower case english letters, '
        'numbers, and @/+/-/_ characters.'
    )
    flags = re.ASCII
