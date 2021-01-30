from rest_framework import serializers
import core.models


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = core.models.Space
        fields = [
            'id', 'name', 'privacy', 'created_on', 'updated_on'
        ]
