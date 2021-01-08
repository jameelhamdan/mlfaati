from django.conf import settings
from app import config as app_config
from datetime import datetime
import json


def config(request):
    return {
        'SITE_NAME': app_config.SITE_NAME,
        'GITHUB_REPO': app_config.GITHUB_REPO,
        'AUTHOR': app_config.AUTHOR,
        'VERSION': app_config.VERSION,
        'YEAR': datetime.today().year,
        'DEBUG': settings.DEBUG,
    }
