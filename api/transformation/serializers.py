from rest_framework import serializers
import processing.models


class TransformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = processing.models.Transformation
        fields = [
            'id', 'type', 'extra_data', 'pipeline_id', 'created_on', 'updated_on'
        ]
