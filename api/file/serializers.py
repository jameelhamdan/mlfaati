from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
import core.models


class UploadSerializer(serializers.ModelSerializer):
    space = serializers.PrimaryKeyRelatedField(queryset=core.models.Space.objects.none(), required=True)

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


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = core.models.File
        fields = [
            'id', 'parent_id', 'name', 'content_type', 'content_length', 'metadata'
        ]
