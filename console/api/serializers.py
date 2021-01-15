from django.urls import reverse
from rest_framework import serializers
import core.models


class ChildrenSerializer(serializers.ModelSerializer):
    serve_url = serializers.SerializerMethodField()

    def get_serve_url(self, obj):
        return obj.get_absolute_url(full=True)

    class Meta:
        model = core.models.File
        fields = ['id', 'name', 'serve_url', 'content_type', 'content_length', 'created_on', 'updated_on']


class FileSerializer(serializers.ModelSerializer):
    serve_url = serializers.SerializerMethodField()
    children = ChildrenSerializer(many=True, default=[])

    def get_serve_url(self, obj):
        return obj.get_absolute_url(full=True)

    class Meta:
        model = core.models.File
        fields = ['id', 'name', 'serve_url', 'children', 'content_type', 'content_length', 'created_on', 'updated_on']


class FolderSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    content_length = serializers.IntegerField(source='files_total_size', default=0)

    def get_url(self, obj):
        return reverse('console:api_browser_folder', kwargs={'pk': obj.space_id, 'folder_id': obj.pk})

    class Meta:
        model = core.models.Folder
        fields = ['id', 'name', 'path', 'url', 'content_length', 'full_path', 'created_on', 'updated_on']
