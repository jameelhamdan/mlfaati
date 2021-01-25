from django.contrib import admin
from . import models


@admin.register(models.Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'user', 'created_on']
    list_select_related = ['user']
    readonly_fields = ['key', 'created_on']
