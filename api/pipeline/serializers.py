from rest_framework import serializers
import processing.models


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = processing.models.Pipeline
        fields = [
            'id', 'name', 'is_enabled', 'target_type', 'folder_id', 'created_on', 'updated_on'
        ]
