import mimetypes
import uuid
import os
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_CREATE
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadToPathAndRename(object):
    def __call__(self, instance: 'File', filename: str) -> str:
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '%s.%s' % (instance.pk, ext)
        # return the whole path to the file
        base_path = str(instance.folder.owner_id)
        return os.path.join(base_path, filename)


class Folder(LifecycleModelMixin, MPTTModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, unique=True, editable=False)
    name = models.CharField(max_length=256, db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='folders')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'parent', 'owner']
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
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, related_name='files')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @hook(BEFORE_CREATE)
    def before_create(self):
        self.name = self.content.name
        self.content_type = mimetypes.guess_type(self.content.name)[0]
        self.content_length = self.content.size

    class Meta:
        unique_together = ['name', 'folder']
        ordering = ['-id']
        verbose_name = _('File')
        verbose_name_plural = _('Files')
        default_permissions = []

    def __str__(self):
        return self.name
