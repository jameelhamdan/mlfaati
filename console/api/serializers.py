from django.urls import reverse
from rest_framework import serializers
import core.models


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = core.models.File
        fields = ['id', 'name', 'content_type', 'content_length', 'created_on', 'updated_on']


class FolderSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('console:api_browser_folder', kwargs={'pk': obj.space_id, 'folder_id': obj.pk})

    class Meta:
        model = core.models.Folder
        fields = ['id', 'name', 'path', 'url', 'full_path', 'created_on', 'updated_on']
