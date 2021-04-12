from rest_framework import serializers
import processing.models


class CreateTransformationSerializer(serializers.ModelSerializer):
    pipeline = serializers.PrimaryKeyRelatedField(
        queryset=processing.models.Pipeline.objects.none(),
        required=True
    )

    class Meta:
        model = processing.models.Transformation
        fields = ['type', 'extra_data', 'pipeline']

    def __init__(self, pipeline_qs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pipeline'].queryset = pipeline_qs


class TransformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = processing.models.Transformation
        fields = [
            'id', 'type', 'extra_data', 'pipeline_id', 'created_on', 'updated_on'
        ]
