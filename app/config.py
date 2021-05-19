from django.conf import settings
from django.urls import reverse_lazy

VERSION = '0.1.1a'
SITE_NAME = 'Mlfaati'
GITHUB_REPO = 'https://github.com/Kingjmk/mlfaati'
DOCS_LINK = reverse_lazy('docs:root')
AUTHOR = 'Jameel Hamdan'
AUTHOR_EMAIL= 'jameelhamdan99@yahoo.com'
PRIVATE_FILE_GET_PARAM = 'token'
ENABLE_TRANSFORMATIONS = getattr(settings, 'ENABLE_TRANSFORMATIONS', True)
ENABLE_ASYNC = getattr(settings, 'ENABLE_ASYNC', True)
