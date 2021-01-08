import uuid
import os

from django.contrib.postgres.fields import ArrayField
from django.db.models import Value, Func, F, Case, When
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_CREATE, BEFORE_UPDATE, AFTER_UPDATE
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.deconstruct import deconstructible
from common import validators

PATH_CONCAT_CHARACTER = '/'


@deconstructible
class UploadToPathAndRename(object):
    def __call__(self, instance: 'File', filename: str) -> str:
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (instance.pk, ext)
        base_path = str(instance.space_id)
        # return the whole path to the file
        return os.path.join(base_path, filename)


class Space(LifecycleModelMixin, models.Model):
    name = models.SlugField(max_length=32, validators=[validators.SpaceNameValidator], unique=True, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='folders')

    class Meta:
        index_together = [['name', 'owner']]
        ordering = ['-id']
        verbose_name = _('Space')
        verbose_name_plural = _('Spaces')
        default_permissions = []

    def __str__(self):
        return self.name


class Folder(LifecycleModelMixin, MPTTModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, unique=True, editable=False)
    name = models.CharField(max_length=256, db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='folders')
    path = ArrayField(
        models.CharField(max_length=256),
        help_text=_('to be used when querying files or folders by path instead of the more efficient id'),
        editable=False, db_index=True
    )

    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)

    @property
    def full_path(self):
        return PATH_CONCAT_CHARACTER.join(self.path) + PATH_CONCAT_CHARACTER

    def get_path(self) -> list:
        """
        Return path of folder (including folder itself)
        :return:
        """
        path = []
        if self.parent:
            path = [a.name for a in self.parent.get_ancestors(include_self=True)]

        return path + [self.name]

    @hook(BEFORE_CREATE)
    def before_create(self):
        # Get initial path of folder
        self.path = self.get_path()

    @hook(BEFORE_UPDATE, when_any=['name', 'parent_id'], has_changed=True)
    def before_update(self):
        self.path = self.get_path()

    @hook(AFTER_UPDATE, when_any=['name', 'parent_id'], has_changed=True)
    def after_update(self):
        self.path = self.get_path()

        # TODO: This is obviously way too slow, so do it in a faster way later
        # update path of children to reflect new parent
        for child in self.get_descendants():
            child.path = child.get_path()
            child.save(update_fields=['path', 'updated_on'])

    class Meta:
        index_together = [['path', 'space']]
        unique_together = [['name', 'parent']]
        ordering = ['-id']
        verbose_name = _('Folder')
        verbose_name_plural = _('Folders')
        default_permissions = []

    def __str__(self):
        return self.name


class File(LifecycleModelMixin, models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, unique=True, editable=False)
    name = models.CharField(max_length=256, db_index=True)
    content_type = models.CharField(max_length=32, db_index=True)
    content_length = models.IntegerField(default=0)
    content = models.FileField(upload_to=UploadToPathAndRename())
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='files')
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)

    def get_path(self):
        folder_path = []
        if self.folder:
            folder_path = self.folder.path

        return PATH_CONCAT_CHARACTER.join(folder_path + [self.name])

    @hook(BEFORE_CREATE)
    def before_create(self):
        self.name = self.content.name
        self.content_type = self.content.file.content_type
        self.content_length = self.content.size

    def get_absolute_url(self):
        return reverse('cdn:by_id', kwargs={'pk': self.pk})

    class Meta:
        unique_together = [['name', 'folder']]
        index_together = [['name', 'folder'], ['name', 'folder', 'space']]
        ordering = ['-id']
        verbose_name = _('File')
        verbose_name_plural = _('Files')
        default_permissions = []

    def __str__(self):
        return self.name
