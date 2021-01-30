from django.urls import path
from rest_framework import generics
from api.generic import (
    BaseAPIView, DetailedCreateAPIView, DetailedUpdateAPIView
)
import core.models
from . import serializers, permissions


class DetailFolderView(BaseAPIView, generics.RetrieveAPIView):
    serializer_class = serializers.ExtendedFolderSerializer
    permission_classes = [permissions.FolderPermission]
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return core.models.Folder.objects.select_related('space', 'parent')


class UpdateFolderView(BaseAPIView, DetailedUpdateAPIView):
    serializer_class = serializers.UpdateFolderSerializer
    detail_serializer = serializers.ExtendedFolderSerializer
    permission_classes = [permissions.FolderPermission]

    def get_queryset(self):
        return core.models.Folder.objects.select_related('space', 'parent')


class CreateFolderView(BaseAPIView, DetailedCreateAPIView):
    serializer_class = serializers.CreateFolderSerializer
    detail_serializer = serializers.ExtendedFolderSerializer
    permission_classes = [permissions.FolderPermission]


urlpatterns = [
    path('detail/<str:pk>', DetailFolderView.as_view(), name='folder_detail'),
    path('update/<str:pk>', UpdateFolderView.as_view(), name='folder_update'),
    path('create', CreateFolderView.as_view(), name='folder_create'),
]
