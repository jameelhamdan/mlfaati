from django.db import models
from django.utils.translation import gettext_lazy as _
from .backends import (all, audio, image, video)


def empty_process_file_function(file, **options):
    return file


def empty_process_metadata_function(file, **options):
    return {}


class TransformationType(models.TextChoices):
    """
    Inorder to bind transformation to action in python
    """

    COMPRESS = 'COMPRESS', _('Compress')
    IMAGE_COMPRESS = 'IMAGE_COMPRESS', _('Compress Image')
    RESIZE = 'RESIZE', _('Resize')
    SCALE = 'SCALE', _('Scale')

    @classmethod
    def file_types(cls):
        return [cls.COMPRESS, cls.IMAGE_COMPRESS, cls.RESIZE, cls.SCALE]

    @classmethod
    def metadata_types(cls):
        return []

    @property
    def fields(self) -> dict:
        fields = {
            self.COMPRESS: {
                'quality': (int,)
            },
            self.IMAGE_COMPRESS: {
                'quality': (int,)
            },
            self.RESIZE: {
                'height': (int,),
                'width': (int,),
            },
            self.SCALE: {
                'scale': (int,)
            }
        }

        return fields.get(self, {})

    @property
    def process_file_function(self):
        if self == self.COMPRESS:
            return empty_process_file_function
        elif self == self.IMAGE_COMPRESS:
            return image.compress
        elif self == self.RESIZE:
            return empty_process_file_function
        elif self == self.SCALE:
            return empty_process_file_function

        return empty_process_file_function

    @property
    def process_metadata_function(self):
        return empty_process_metadata_function


class FileType(models.TextChoices):
    """
    File types that the pipeline will work on
    """
    ALL = 'ALL', _('All')
    IMAGE = 'IMAGE', _('Image')
    VIDEO = 'VIDEO', _('Video')
    AUDIO = 'AUDIO', _('Audio')

    @property
    def mapping(self) -> list:
        mapping = {
            self.ALL: [TransformationType.COMPRESS],
            self.IMAGE: [
                TransformationType.IMAGE_COMPRESS,
                TransformationType.RESIZE,
                TransformationType.SCALE
            ],
        }

        return mapping.get(self, [])

    @classmethod
    def get_file_type(cls, content_type: 'str') -> 'FileType':
        # TODO: detect file type more robustly
        if 'image' in content_type:
            return cls.IMAGE
        elif 'video' in content_type:
            return cls.VIDEO
        elif 'audio' in content_type:
            return cls.AUDIO

        return cls.ALL
