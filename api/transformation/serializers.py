from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
import processing.models


class CreateTransformationSerializer(serializers.ModelSerializer):
    pipeline = serializers.PrimaryKeyRelatedField(
        queryset=processing.models.Pipeline.objects.none(),
        required=True
    )

    def validate(self, data):
        transform_type = processing.models.Transformation.TYPES(data['type'])
        pipeline = data['pipeline']
        extra_data = data.get('extra_data', {})

        if transform_type.value not in pipeline._target_type.mapping:
            raise serializers.ValidationError({'type': _('Type is not supported by selected pipeline.')})

        # TODO: improve how extra_data errors show in response
        processing.models.Transformation.validate_extra_data(transform_type, extra_data)

        return data

    class Meta:
        model = processing.models.Transformation
        fields = ['type', 'extra_data', 'pipeline']

    def __init__(self, pipeline_qs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pipeline'].queryset = pipeline_qs


class TransformationSerializer(serializers.ModelSerializer):
    def validate(self, data):
        transform_type = processing.models.Transformation.TYPES(data['type'])
        extra_data = data.get('extra_data', {})

        if transform_type.value not in self.instance.pipeline._target_type.mapping:
            raise serializers.ValidationError({'type': _('Type is not supported by selected pipeline.')})

        # TODO: improve how extra_data errors show in response
        processing.models.Transformation.validate_extra_data(transform_type, extra_data)

        return data

    class Meta:
        model = processing.models.Transformation
        fields = [
            'id', 'type', 'extra_data', 'created_on', 'updated_on'
        ]
