from django.db import models
from django.utils.translation import gettext_lazy as _


class TransformationType(models.TextChoices):
    """
    Inorder to bind transformation to action in python
    """

    COMPRESS = 'COMPRESS', _('Compress')
    IMAGE_COMPRESS = 'IMAGE_COMPRESS', _('Compress Image')
    RESIZE = 'RESIZE', _('Resize')
    SCALE = 'SCALE', _('Scale')

    @classmethod
    def get_field_mapping(cls) -> dict:
        return {
            cls.COMPRESS: [],
            cls.IMAGE_COMPRESS: [],
            cls.RESIZE: [],
            cls.SCALE: [],
        }

    @classmethod
    def get_fields(cls, transformation: 'TransformationType'):
        # TODO: map values in a better way allowing validation, forms maybe?
        return cls.get_field_mapping()[transformation]


class FileType(models.TextChoices):
    """
    File types that the pipeline will work on
    """
    ALL = 'ALL', _('All')
    IMAGE = 'IMAGE', _('Image')
    VIDEO = 'VIDEO', _('Video')
    AUDIO = 'AUDIO', _('Audio')

    @classmethod
    def get_transformation_mapping(cls) -> dict:
        return {
            cls.ALL: [TransformationType.COMPRESS],
            cls.IMAGE: [
                TransformationType.IMAGE_COMPRESS,
                TransformationType.RESIZE,
                TransformationType.SCALE
            ],
            cls.VIDEO: [],
            cls.AUDIO: [],
        }

    @classmethod
    def get_allowed_operations(cls, content_type: 'str') -> list:
        mapping = cls.get_transformation_mapping()

        # TODO: detect file type more robustly
        if 'image' in content_type:
            return mapping[cls.IMAGE]
        elif 'video' in content_type:
            return mapping[cls.VIDEO]
        elif 'audio' in content_type:
            return mapping[cls.AUDIO]

        return mapping[cls.ALL]
