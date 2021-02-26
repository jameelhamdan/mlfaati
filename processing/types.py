from django.db import models
from django.utils.translation import gettext_lazy as _


class ChecksumType(models.TextChoices):
    MD5 = 'MD5', _('MD5')
    SHA256 = 'SHA256', _('SHA256')
