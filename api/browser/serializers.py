from rest_framework import serializers
import core.models


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = core.models.Folder
        fields = [
            'id', 'name', 'path', 'full_path', 'created_on', 'updated_on'
        ]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = core.models.File
        fields = [
            'id', 'parent_id', 'name', 'content_type', 'content_length', 'metadata'
        ]
