from django.contrib import admin
from django.utils.html import format_html
from . import models


@admin.register(models.Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'privacy']
    list_select_related = ['owner']
    list_filter = ['owner']
    search_fields = ['name']


@admin.register(models.Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_path', 'space']
    list_select_related = ['parent', 'space']
    list_filter = ['name', 'parent', 'space']
    search_fields = ['name']


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'space', 'path', 'parent', 'cdn_url']
    list_select_related = ['folder', 'space', 'parent']
    readonly_fields = ['name', 'parent', 'content_type', 'content_length']
    list_filter = ['name', 'content_type', 'folder']
    autocomplete_fields = ['folder']

    def cdn_url(self, obj):
        return format_html('<a href="{url}">Link</a>', url=obj.get_absolute_url())

    def path(self, obj):
        return obj.get_path()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['content']
        return self.readonly_fields
