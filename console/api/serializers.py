from django.urls import reverse
from rest_framework import serializers
import core.models
import processing.models


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = processing.models.Pipeline
        fields = ['id', 'name', 'target_type']


class ChildrenSerializer(serializers.ModelSerializer):
    serve_url = serializers.SerializerMethodField()
    pipeline = PipelineSerializer()

    def get_serve_url(self, obj):
        return obj.get_absolute_url(full=True)

    class Meta:
        model = core.models.File
        fields = ['id', 'name', 'serve_url', 'pipeline', 'content_type', 'content_length', 'created_on', 'updated_on']


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
    files_count = serializers.IntegerField(default=0)
    files_total_size = serializers.IntegerField(default=0)

    def get_url(self, obj):
        return reverse('console:api_browser_folder', kwargs={'pk': obj.space_id, 'folder_id': obj.pk})

    class Meta:
        model = core.models.Folder
        fields = ['id', 'name', 'path', 'url', 'files_count', 'files_total_size', 'full_path', 'created_on', 'updated_on']
