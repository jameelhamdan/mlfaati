from django.conf import settings
from django.utils.translation import gettext_lazy as _

VERSION = '0.0.3a'
SITE_NAME = _('Mlfaati')
GITHUB_REPO = 'https://github.com/Kingjmk/mlfaati'
AUTHOR = 'Jameel Hamdan'
PRIVATE_FILE_GET_PARAM = 'token'
ENABLE_TRANSFORMATIONS = getattr(settings, 'ENABLE_TRANSFORMATIONS', True)
ENABLE_ASYNC = getattr(settings, 'ENABLE_ASYNC', True)
