from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_lifecycle import LifecycleModelMixin
import core.models
from common import validators
from . import definitions


class Pipeline(LifecycleModelMixin, models.Model):
    """
    Model to store pipeline for folder,
    purpose of pipeline is to enable running multiple transformations on the same file as a _pipeline_
    and outputting a file as a result
    """

    TYPES = definitions.FileType

    name = models.SlugField(max_length=20, validators=[validators.PipelineNameValidator])
    is_enabled = models.BooleanField(default=True, db_index=True)
    target_type = models.CharField(
        choices=TYPES.choices,
        max_length=16,
        db_index=True,
        help_text=_('Select which kind of files to use for this Pipeline')
    )
    folder: 'core.models.Folder' = models.ForeignKey(
        'core.Folder',
        on_delete=models.CASCADE,
        related_name='pipelines'
    )

    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)

    @property
    def _target_type(self) -> definitions.FileType:
        return self.TYPES(self.target_type)

    class Meta:
        constraints = [
            UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_name_folder',
                fields=['name', 'folder'],
            ),
        ]
        ordering = ['-id']
        verbose_name = _('Pipeline')
        verbose_name_plural = _('Pipelines')
        default_permissions = []

    def __str__(self):
        return self.name


class Transformation(LifecycleModelMixin, models.Model):
    """
    Model to store transformation processes for folder
    """
    TYPES = definitions.TransformationType

    pipeline: 'Pipeline' = models.ForeignKey('Pipeline', on_delete=models.CASCADE, related_name='transformations')
    type = models.CharField(choices=TYPES.choices, max_length=16, db_index=True)
    extra_data = models.JSONField(
        default=dict,
        help_text=_("transformation configuration (Shouldn\'t) be manually edited)"),
        blank=True
    )

    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)

    @property
    def _type(self) -> definitions.TransformationType:
        return self.TYPES(self.type)

    def process_metadata(self, file):
        return self._type.process_metadata_function(file, **self.extra_data)

    def process_file(self, file):
        return self._type.process_file_function(file, **self.extra_data)

    def clean(self):
        if self.type and self.type not in self.pipeline._target_type.mapping:
            raise ValidationError({'type': _('Type is not supported by selected pipeline.')})

        self.validate_extra_data(self._type, self.extra_data)

    @classmethod
    def validate_extra_data(cls, _type: 'definitions.TransformationType', data: dict):
        errors = []

        serializer = _type.serializer(data=data)
        serializer.is_valid(raise_exception=False)

        if serializer.errors:
            for field, error in serializer.errors.items():
                error_detail = error[0]
                errors += ValidationError('%(field_name)s: %(error)s', params={
                    'field_name': field,
                    'error': error_detail,
                }, code=getattr(error_detail, 'code', None))

            raise ValidationError({'extra_data': errors})

        return data

    class Meta:
        ordering = ['-id']
        verbose_name = _('Transformation')
        verbose_name_plural = _('Transformations')
        default_permissions = []
