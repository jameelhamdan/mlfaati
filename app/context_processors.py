from django.conf import settings
from app import config as app_config


def config(request):
    return {
        'SITE_NAME': app_config.SITE_NAME,
        'GITHUB_REPO': app_config.GITHUB_REPO,
        'DOCS_LINK': app_config.DOCS_LINK,
        'AUTHOR': app_config.AUTHOR,
        'AUTHOR_EMAIL': app_config.AUTHOR_EMAIL,
        'VERSION': app_config.VERSION,
        'DEBUG': settings.DEBUG,
    }
