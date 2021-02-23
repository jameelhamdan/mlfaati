"""

Serializers for validating transform types

"""
from rest_framework import serializers
from .types import ChecksumType


class BaseSerializer(serializers.Serializer):
    pass


# General Serializer
class CompressSerializer(BaseSerializer):
    quality = serializers.IntegerField(required=True, min_value=1, max_value=100)


class ChecksumSerializer(BaseSerializer):
    type = serializers.ChoiceField(required=True, choices=ChecksumType.choices)


# Image Serializer
class ImageCompressSerializer(BaseSerializer):
    quality = serializers.IntegerField(required=True, min_value=1, max_value=100)


class ImageResizeSerializer(BaseSerializer):
    height = serializers.IntegerField(required=True, min_value=1)
    width = serializers.IntegerField(required=True, min_value=1)
    upscale = serializers.BooleanField(required=True)


class ImageAdjustSerializer(BaseSerializer):
    color = serializers.FloatField(required=True, min_value=0)
    brightness = serializers.FloatField(required=True, min_value=1)
    contrast = serializers.FloatField(required=True, min_value=1)
    sharpness = serializers.FloatField(required=True, min_value=1)
