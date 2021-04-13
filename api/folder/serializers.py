from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
import core.models


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = core.models.Folder
        fields = [
            'id', 'name', 'path', 'full_path', 'created_on', 'updated_on'
        ]


class ExtendedFolderSerializer(serializers.ModelSerializer):
    parent = FolderSerializer(
        default=None, help_text=_('Parent folder'),
    )

    class Meta:
        model = core.models.Folder
        fields = [
            'id', 'name', 'path', 'full_path', 'created_on', 'updated_on', 'parent', 'space_id'
        ]


class UpdateFolderSerializer(serializers.ModelSerializer):
    def validate_name(self, name):
        # Check unique constraint
        qs = self.__class__.Meta.model.objects.filter(
            parent_id=self.instance.parent_id,
            space_id=self.instance.space_id
        ).exclude(
            pk=self.instance.pk
        )

        if name and qs.filter(name=name).exists():
            raise serializers.ValidationError(
                _('Parent Folder already has child with same name.'), code='unique_together'
            )

        return name

    class Meta:
        model = core.models.Folder
        fields = ['name']


class CreateFolderSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # Check unique constraint

        space = data['space']
        parent = data.get('parent', None)
        name = data['name']

        if parent and space.id != parent.space_id:
            raise serializers.ValidationError(
                {'folder': _('Parent folder does not belong to the selected space.')}
            )

        qs = self.__class__.Meta.model.objects.filter(parent=parent, space_id=space.id)

        if name and qs.filter(name=name).exists():
            raise serializers.ValidationError(
                {'name': _('Parent Folder already has child with same name.')}, code='unique_together'
            )

        return data

    class Meta:
        model = core.models.Folder
        fields = ['name', 'parent', 'space']
