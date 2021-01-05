from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

AlphaValidator = RegexValidator(r'^[a-zA-Z ]*$', _('Only english characters are allowed.'))
