from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
import core.models


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = core.models.Folder
        fields = [
            'id', 'name', 'path', 'full_path', 'created_on', 'updated_on'
        ]


class ExtendedFolderSerializer(serializers.ModelSerializer):
    parent = FolderSerializer(
        default=None, help_text=_('Parent folder'),
    )

    class Meta:
        model = core.models.Folder
        fields = [
            'id', 'name', 'path', 'full_path', 'created_on', 'updated_on', 'parent', 'space'
        ]


class UpdateFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = core.models.Folder
        fields = ['name']


class CreateFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = core.models.Folder
        fields = ['name', 'parent', 'space']
