from .celery import app as celery_app

__all__ = ['celery_app', 'config', 'context_processors', 'server', 'staticfiles', 'urls']
