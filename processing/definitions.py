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
    CHECKSUM = 'CHECKSUM', _('Check sum')
    IMAGE_COMPRESS = 'IMAGE_COMPRESS', _('Compress Image')
    IMAGE_CLASSIFY = 'IMAGE_CLASSIFY', _('Classify Image')
    RESIZE = 'RESIZE', _('Resize')
    ADJUST = 'ADJUST', _('Adjust')

    @classmethod
    def file_types(cls):
        return [cls.COMPRESS, cls.IMAGE_COMPRESS, cls.RESIZE, cls.ADJUST]

    @classmethod
    def metadata_types(cls):
        return [cls.IMAGE_CLASSIFY, cls.CHECKSUM]

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
                'upscale': (bool, )
            },
            self.ADJUST: {
                'color': (float,),
                'brightness': (float,),
                'contrast': (float,),
                'sharpness': (float,)
            },
            self.CHECKSUM: {
                'type': (str, )  # Must be MD5, or SHA256
            },
            self.IMAGE_CLASSIFY: {},
        }

        return fields.get(self, {})

    @property
    def process_file_function(self):
        if self == self.COMPRESS:
            return all.compress
        elif self == self.IMAGE_COMPRESS:
            return image.compress
        elif self == self.RESIZE:
            return image.resize
        elif self == self.ADJUST:
            return image.adjust

        return empty_process_file_function

    @property
    def process_metadata_function(self):
        if self == self.IMAGE_CLASSIFY:
            return image.classify
        elif self == self.CHECKSUM:
            return all.checksum
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
            self.ALL: [
                TransformationType.COMPRESS,
                TransformationType.CHECKSUM,
            ],
            self.IMAGE: [
                TransformationType.IMAGE_COMPRESS,
                TransformationType.RESIZE,
                TransformationType.ADJUST,
                TransformationType.IMAGE_CLASSIFY,
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
