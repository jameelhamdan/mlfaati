from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from . import models


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'folder']
    list_select_related = ['folder']
    readonly_fields = ['name', 'content_type', 'content_length']
    list_filter = ['name', 'content_type', 'folder']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['content']
        return self.readonly_fields


@admin.register(models.Folder)
class FolderAdmin(MPTTModelAdmin):
    list_display = ['name', 'full_path', 'owner']
    list_select_related = ['parent', 'owner']
    list_filter = ['name', 'parent', 'owner']
