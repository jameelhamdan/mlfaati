from django.contrib.staticfiles.storage import StaticFilesStorage as BaseStaticFilesStorage
from app import config


class StaticFilesStorage(BaseStaticFilesStorage):
    def url(self, name):
        return '%s?v=%s' % (super().url(name), config.VERSION)
