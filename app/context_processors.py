from django.conf import settings
from app import config as app_config
from datetime import datetime
import json


def config(request):
    return {
        'YEAR': datetime.today().year,
        'DEBUG': settings.DEBUG,
        'VERSION': app_config.VERSION,
    }
