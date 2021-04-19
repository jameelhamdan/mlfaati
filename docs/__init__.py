"""
Docs App, used to build and serve docs
"""
import os
from django.conf import settings

DOCS_ROOT = os.path.join(settings.BASE_DIR, 'docs/_build')
