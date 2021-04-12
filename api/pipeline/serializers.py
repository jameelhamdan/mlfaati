from rest_framework import serializers
import core.models
import processing.models
from api.transformation.serializers import TransformationSerializer
from django.utils.translation import gettext_lazy as _


class PipelineSerializer(serializers.ModelSerializer):
    folder = serializers.PrimaryKeyRelatedField(
        queryset=core.models.Folder.objects.none(),
        required=True
    )

    def validate(self, data):
        folder, name = data['folder'], data['name']

        pipeline_qs = folder.pipelines.all()
        if self.instance and self.instance.pk:
            pipeline_qs = pipeline_qs.exclude(id=self.instance.pk)

        if pipeline_qs.filter(name=name).exists():
            raise serializers.ValidationError(
                {'folder': _('Pipeline with the same name exists on this folder.')}
            )

        return data

    class Meta:
        model = processing.models.Pipeline
        fields = [
            'id', 'name', 'is_enabled', 'target_type', 'folder', 'created_on', 'updated_on'
        ]

    def __init__(self, folder_qs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].queryset = folder_qs


class UpdatePipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = processing.models.Pipeline
        fields = [
            'name', 'is_enabled', 'target_type'
        ]


class ExtendedPipelineSerializer(serializers.ModelSerializer):
    transformations = TransformationSerializer(many=True, default=[], read_only=True)

    class Meta:
        model = processing.models.Pipeline
        fields = [
            'id', 'name', 'is_enabled', 'target_type', 'folder_id', 'created_on', 'updated_on',
            'transformations'
        ]
