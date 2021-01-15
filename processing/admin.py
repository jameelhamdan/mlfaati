from django.contrib import admin
from . import models


@admin.register(models.Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ['name', 'target_type', 'folder', 'is_enabled']
    list_select_related = ['folder']
    list_filter = ['is_enabled']
    search_fields = ['name']
    autocomplete_fields = ['folder']


@admin.register(models.Transformation)
class TransformationAdmin(admin.ModelAdmin):
    list_display = ['pipeline', 'type']
    list_select_related = ['pipeline']
    list_filter = ['type']
    autocomplete_fields = ['pipeline']
