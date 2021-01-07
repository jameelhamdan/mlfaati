from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin
from . import models


@admin.register(models.Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    list_select_related = ['owner']
    list_filter = ['owner']
    search_fields = ['name']


@admin.register(models.Folder)
class FolderAdmin(MPTTModelAdmin):
    list_display = ['name', 'full_path', 'space']
    list_select_related = ['parent', 'space']
    list_filter = ['name', 'parent', 'space']
    search_fields = ['name']


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'folder_path', 'cdn_url']
    list_select_related = ['folder']
    readonly_fields = ['name', 'content_type', 'content_length']
    list_filter = ['name', 'content_type', 'folder']
    autocomplete_fields = ['folder']

    def cdn_url(self, obj):
        return format_html('<a href="{url}">{url}</a>', url=obj.get_absolute_url())

    def folder_path(self, obj):
        return obj.folder_path

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['content']
        return self.readonly_fields

    def get_queryset(self, request):
        return super().get_queryset(request).with_paths()

