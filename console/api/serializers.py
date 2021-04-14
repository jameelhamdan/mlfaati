from django.urls import reverse
from rest_framework import serializers
import core.models
import processing.models
from django.utils.translation import gettext_lazy as _


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
        fields = ['id', 'name', 'short_name', 'serve_url', 'pipeline', 'content_type', 'content_length', 'created_on', 'updated_on']


class FileSerializer(serializers.ModelSerializer):
    serve_url = serializers.SerializerMethodField()
    children = ChildrenSerializer(many=True, default=[])

    def get_serve_url(self, obj):
        return obj.get_absolute_url(full=True)

    class Meta:
        model = core.models.File
        fields = ['id', 'name', 'short_name', 'serve_url', 'children', 'content_type', 'content_length', 'created_on', 'updated_on']


class FolderSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    update_url = serializers.SerializerMethodField()
    files_count = serializers.IntegerField(default=0)
    files_total_size = serializers.IntegerField(default=0)

    def get_url(self, obj):
        return reverse('console:api_browser_folder', kwargs={'pk': obj.space_id, 'folder_id': obj.pk})

    def get_update_url(self, obj):
        return reverse('console:api_folder_update', kwargs={'pk': obj.pk})

    class Meta:
        model = core.models.Folder
        fields = [
            'id', 'name', 'path', 'url', 'files_count', 'files_total_size', 'full_path',
            'update_url', 'created_on', 'updated_on'
        ]


class CreateFolderSerializer(serializers.ModelSerializer):
    space = serializers.PrimaryKeyRelatedField(queryset=core.models.Space.objects.none(), required=True)

    def validate(self, data):
        """
        Check that Folder is within same space
        """
        name = data.get('name')
        space = data.get('space')
        parent_folder = data.get('parent')

        if not space:
            return data

        if parent_folder:
            if space.id != parent_folder.space_id:
                raise serializers.ValidationError({'parent': _('Parent folder does not belong to the selected space.')})

        # Check unique constraint
        qs = core.models.Folder.objects.filter(parent_id=parent_folder, space_id=space.id)

        if name and qs.filter(name=name).exists():
            raise serializers.ValidationError(
                {'name':  _('Parent Folder already has child with same name.')}, code='unique_together'
            )

        return data

    class Meta:
        model = core.models.Folder
        fields = ['name', 'parent', 'space']

    def __init__(self, space_qs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['space'].queryset = space_qs


class UpdateFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = core.models.Folder
        fields = ['name']


class CreateFileSerializer(serializers.ModelSerializer):
    space = serializers.PrimaryKeyRelatedField(queryset=core.models.Space.objects.none(), required=True)
    content = serializers.FileField(
        required=True, error_messages={
            'required': _('File is required.')
        }
    )

    def validate(self, data):
        parent_folder = data.get('folder')
        space = data['space']

        if parent_folder and space.id != parent_folder.space_id:
            raise serializers.ValidationError(
                {'folder': _('Parent folder does not belong to the selected space.')}
            )

        return data

    class Meta:
        model = core.models.File
        fields = ['folder', 'content', 'space']

    def __init__(self, space_qs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['space'].queryset = space_qs
