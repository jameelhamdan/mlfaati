from django.conf import settings


VERSION = '0.0.6a'
SITE_NAME = 'Mlfaati'
GITHUB_REPO = 'https://github.com/Kingjmk/mlfaati'
AUTHOR = 'Jameel Hamdan'
PRIVATE_FILE_GET_PARAM = 'token'
ENABLE_TRANSFORMATIONS = getattr(settings, 'ENABLE_TRANSFORMATIONS', True)
ENABLE_ASYNC = getattr(settings, 'ENABLE_ASYNC', True)
