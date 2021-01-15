import uuid
import os
from datetime import timedelta
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_CREATE, BEFORE_UPDATE, AFTER_UPDATE
from django.utils.deconstruct import deconstructible
from tree_queries.models import TreeNode, TreeNodeForeignKey

from app import config
from common import validators, crypt

PATH_CONCAT_CHARACTER = '/'


class FileAccessError(Exception):
    pass


@deconstructible
class UploadToPathAndRename(object):
    def __call__(self, instance: 'File', filename: str) -> str:
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (instance.pk, ext)
        base_path = str(instance.space_id)
        # return the whole path to the file
        return os.path.join(base_path, filename)


class SpaceQueryset(models.QuerySet):
    def owned(self, user):
        return self.filter(owner_id=user.pk)


class Space(LifecycleModelMixin, models.Model):
    class PRIVACY(models.TextChoices):
        PUBLIC = 'PUBLIC', _('Public')
        PRIVATE = 'PRIVATE', _('Private')

        @classmethod
        def as_dict(cls):
            return {
                cls.PUBLIC.name: cls.PUBLIC.value,
                cls.PRIVATE.name: cls.PRIVATE.value,
            }

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, unique=True, editable=False)
    privacy = models.CharField(
        max_length=10, choices=PRIVACY.choices, default=PRIVACY.PUBLIC, db_index=True,
        help_text=_('Whether files inside space can be accessed publicly')
    )

    name = models.SlugField(max_length=32, validators=[validators.SpaceNameValidator], unique=True, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='folders')

    objects = SpaceQueryset.as_manager()

    class Meta:
        index_together = [['name', 'owner']]
        ordering = ['-id']
        verbose_name = _('Space')
        verbose_name_plural = _('Spaces')
        default_permissions = []

    def __str__(self):
        return self.name


class Folder(LifecycleModelMixin, TreeNode):
    name = models.CharField(max_length=256, db_index=True)
    parent: 'Folder' = TreeNodeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )
    space: 'Space' = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='folders')
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
            path = [a.name for a in self.parent.ancestors(include_self=True)]

        return path + [self.name]

    @hook(BEFORE_CREATE)
    def before_create(self):
        # Get initial path of folder
        self.path = self.get_path()

    @hook(BEFORE_UPDATE, when_any=['name', 'parent_id'], has_changed=True)
    def before_name_or_parent_update(self):
        self.path = self.get_path()

    @hook(AFTER_UPDATE, when_any=['name', 'parent_id'], has_changed=True)
    def after_name_or_parent_update(self):
        self.path = self.get_path()

        # TODO: This is obviously way too slow, so do it in a faster way later
        # update path of children to reflect new parent
        for child in self.descendants().iterator():
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
    folder: 'Folder' = TreeNodeForeignKey('Folder', on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='files')
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)

    def get_path(self, with_space: bool = True):
        folder_path = []
        if self.folder:
            folder_path = self.folder.path

        if with_space:
            return PATH_CONCAT_CHARACTER.join([self.space.name] + folder_path + [self.name])
        return PATH_CONCAT_CHARACTER.join(folder_path + [self.name])

    @hook(BEFORE_CREATE)
    def before_create(self):
        self.name = self.content.name
        self.content_type = self.content.file.content_type
        self.content_length = self.content.size

    def get_absolute_url(self, access_time: int = 900, full: bool = False):
        """
        Gets serve url for public and private files
        :param access_time: how long in minutes the access will remain (for private files)
        :param full: return full path url or return only with uuid
        :return: url
        """

        url = reverse('cdn:by_id', kwargs={'pk': self.pk})
        if full:

            url = reverse('cdn:by_path', kwargs={
                'space_name': self.space.name,
                'path': self.get_path(False)

            })

        if self.space.privacy == self.space.PRIVACY.PRIVATE:
            return '%s?%s=%s' % (url, config.PRIVATE_FILE_GET_PARAM, self.get_access_token(access_time))

        return url

    def get_access_token(self, minutes: int = 1440) -> str:
        """
        Create unconditional access token for x minutes
        :param minutes: int number of minutes to allow access to private file
        :return: Base64 encoded token
        """
        return crypt.encode_token({
            'uuid': str(self.pk),
            'space_id': str(self.space_id),
        }, timedelta(minutes=minutes))

    def verify_access_token(self, token):
        """
        Check whether token is valid for this File
        :param token: Base64 encoded Token from get_access_token
        """
        try:
            data = crypt.verify_token(token)
        except crypt.jwt_exceptions.PyJWTError as e:
            raise FileAccessError() from e
        if data['uuid'] != str(self.pk) or data['space_id'] != str(self.space_id):
            raise FileAccessError()

    class Meta:
        unique_together = [['name', 'folder']]
        index_together = [['name', 'folder'], ['name', 'folder', 'space']]
        ordering = ['-id']
        verbose_name = _('File')
        verbose_name_plural = _('Files')
        default_permissions = []

    def __str__(self):
        return self.name
