from django.conf import settings
from app import config as app_config


def config(request):
    return {
        'SITE_NAME': app_config.SITE_NAME,
        'GITHUB_REPO': app_config.GITHUB_REPO,
        'AUTHOR': app_config.AUTHOR,
        'VERSION': app_config.VERSION,
        'DEBUG': settings.DEBUG,
    }
