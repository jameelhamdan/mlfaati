import uuid
import os
from datetime import timedelta
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db.models import UniqueConstraint, Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models, transaction
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_CREATE, AFTER_CREATE, BEFORE_UPDATE, AFTER_UPDATE
from django.utils.deconstruct import deconstructible
from tree_queries.models import TreeNode, TreeNodeForeignKey, TreeQuerySet
from app import config
from common import validators, crypt
import processing.tasks
from common.crypt import short_uuid
import processing.definitions
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


class FolderQueryset(TreeQuerySet):
    def owned(self, user):
        return self.filter(space__owner_id=user.pk)


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

    objects = FolderQueryset.as_manager()

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

    def _perform_unique_checks(self, unique_checks):
        errors = super()._perform_unique_checks(unique_checks)
        qs = self.__class__.objects.filter(name=self.name)
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if self.parent_id:
            qs = qs.filter(parent_id=self.parent_id)
        else:
            qs = qs.filter(parent_id__isnull=True)

        error_already_raised = False

        if NON_FIELD_ERRORS in errors.keys() and errors[NON_FIELD_ERRORS][0].code == 'unique_together':
            error_already_raised = True

        if not error_already_raised and qs.exists():
            errors.setdefault(NON_FIELD_ERRORS, []).append(
                ValidationError(_('Folder with this Name and Parent already exists.'), code='unique_together')
            )

        return errors

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
        constraints = [
            UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_name_parent_nullable',
                fields=['name'],
                condition=Q(parent__isnull=True)
            ),
            UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_name_parent',
                fields=['name', 'parent'],
            ),
        ]
        ordering = ['-id']
        verbose_name = _('Folder')
        verbose_name_plural = _('Folders')
        default_permissions = []

    def __str__(self):
        return self.name


class File(LifecycleModelMixin, models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, unique=True, editable=False)
    name = models.CharField(max_length=256, db_index=True)
    content_type = models.CharField(max_length=144, db_index=True)
    content_length = models.IntegerField(default=0)
    content = models.FileField(upload_to=UploadToPathAndRename())
    metadata = models.JSONField(default=dict, blank=True)

    folder: 'Folder' = models.ForeignKey('Folder', on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    space: 'Space' = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='files')

    # Fields for child files
    parent: 'File' = models.ForeignKey(
        'File', on_delete=models.CASCADE, related_name='children', null=True, blank=True, editable=False,
        help_text=_('For processed files parent')
    )
    pipeline = models.ForeignKey(
        'processing.Pipeline', on_delete=models.CASCADE, related_name='files', null=True, blank=True, editable=False,
    )

    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)

    def get_path(self, with_space: bool = True):
        folder_path = []
        if self.folder:
            folder_path = self.folder.path

        if with_space:
            return PATH_CONCAT_CHARACTER.join([self.space.name] + folder_path + [self.name])
        return PATH_CONCAT_CHARACTER.join(folder_path + [self.name])

    @classmethod
    def check_name_exists(cls, folder_id, file_name):
        return cls.objects.filter(folder_id=folder_id, name=file_name).exists()

    @classmethod
    def get_alternative_name(cls, name):
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        return '%s_%s%s' % (file_root, short_uuid(), file_ext)

    def get_file_type(self) -> 'processing.definitions.FileType':
        """
        Returns processing.definitions.FileType
        """
        return processing.definitions.FileType.get_file_type(self.content_type)

    @hook(BEFORE_CREATE)
    def before_create(self):
        self.name = self.content.name

        if self.check_name_exists(self.folder_id, self.name):
            self.name = self.get_alternative_name(self.name)

        self.content_type = self.content.file.content_type
        self.content_length = self.content.size

    @hook(AFTER_CREATE)
    def after_create(self):
        if not config.ENABLE_TRANSFORMATIONS:
            return

        if self.parent_id or not self.folder_id:
            return

        if config.ENABLE_ASYNC:
            transaction.on_commit(lambda: processing.tasks.process_file.delay(self.pk))
        else:
            processing.tasks.process_file(self.pk)

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

        return True

    class Meta:
        index_together = [['name', 'folder'], ['name', 'folder', 'space']]
        constraints = [
            UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_name_folder_nullable',
                fields=['name'],
                condition=Q(folder__isnull=True),
            ),
            UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_name_folder',
                fields=['name', 'folder'],
            ),
        ]
        ordering = ['-id']
        verbose_name = _('File')
        verbose_name_plural = _('Files')
        default_permissions = []

    def __str__(self):
        return self.name
