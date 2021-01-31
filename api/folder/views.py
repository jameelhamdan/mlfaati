from django.urls import path
from rest_framework import generics, response, status
from django.utils.translation import gettext_lazy as _
from api.generic import (
    BaseAPIView, DetailedCreateAPIView, DetailedUpdateAPIView
)
import core.models
from . import serializers, permissions


class CreateFolderView(BaseAPIView, DetailedCreateAPIView):
    serializer_class = serializers.CreateFolderSerializer
    detail_serializer = serializers.ExtendedFolderSerializer
    permission_classes = [permissions.FolderPermission]


class DetailFolderView(BaseAPIView, generics.RetrieveAPIView):
    serializer_class = serializers.ExtendedFolderSerializer
    permission_classes = [permissions.FolderPermission]
    lookup_url_kwarg = 'pk'
    queryset = core.models.Folder.objects.select_related('space', 'parent')


class UpdateFolderView(BaseAPIView, DetailedUpdateAPIView):
    serializer_class = serializers.UpdateFolderSerializer
    detail_serializer = serializers.ExtendedFolderSerializer
    permission_classes = [permissions.FolderPermission]
    queryset = core.models.Folder.objects.select_related('space', 'parent')


class DeleteFolderView(BaseAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.FolderPermission]
    queryset = core.models.Folder.objects.select_related('space')
    lookup_url_kwarg = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.descendants().count() > 0:
            return response.Response(
                {
                    'message': _('This Folder is not empty.'),
                    'code': 'contains_folders',
                },
                status=status.HTTP_409_CONFLICT
            )

        if instance.files.count() > 0:
            return response.Response(
                {
                    'message': _('This Folder is not empty.'),
                    'code': 'contains_files',
                },
                status=status.HTTP_409_CONFLICT
            )

        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


urlpatterns = [
    path('create', CreateFolderView.as_view(), name='folder_create'),
    path('<str:pk>', DetailFolderView.as_view(), name='folder_detail'),
    path('<str:pk>/update', UpdateFolderView.as_view(), name='folder_update'),
    path('<str:pk>/delete', DeleteFolderView.as_view(), name='folder_delete'),
]
