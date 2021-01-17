from django.db import models
from django.utils.translation import gettext_lazy as _
from .backends import (all, audio, image, video)


def empty_process_function(file, **options):
    return file


class TransformationType(models.TextChoices):
    """
    Inorder to bind transformation to action in python
    """

    COMPRESS = 'COMPRESS', _('Compress')
    IMAGE_COMPRESS = 'IMAGE_COMPRESS', _('Compress Image')
    RESIZE = 'RESIZE', _('Resize')
    SCALE = 'SCALE', _('Scale')

    @property
    def fields(self) -> dict:
        if self == self.COMPRESS:
            return {
                'quality': (int,)
            }
        elif self == self.IMAGE_COMPRESS:
            return {
                'quality': (int,)
            }
        elif self == self.RESIZE:
            return {
                'height': (int,),
                'width': (int,),
            }
        elif self == self.SCALE:
            return {
                'scale': (int,)
            }

        return {}

    @property
    def process_function(self):
        if self == self.COMPRESS:
            return empty_process_function
        elif self == self.IMAGE_COMPRESS:
            return image.compress
        elif self == self.RESIZE:
            return empty_process_function
        elif self == self.SCALE:
            return empty_process_function

        return empty_process_function


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
        if self == self.ALL:
            return [TransformationType.COMPRESS]
        elif self == self.IMAGE:
            return [
                TransformationType.IMAGE_COMPRESS,
                TransformationType.RESIZE,
                TransformationType.SCALE
            ]
        elif self == self.VIDEO:
            return []
        elif self == self.AUDIO:
            return []

        return []

    @classmethod
    def get_allowed_operations(cls, content_type: 'str') -> list:
        mapping = cls.get_transformation_mapping()

        # TODO: detect file type more robustly
        if 'image' in content_type:
            return cls.IMAGE.mapping
        elif 'video' in content_type:
            return cls.VIDEO.mapping
        elif 'audio' in content_type:
            return cls.AUDIO.mapping

        return mapping[cls.ALL]
