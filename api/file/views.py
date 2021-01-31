from django.urls import path
from api.generic import BaseAPIView, DetailedCreateAPIView
from rest_framework import generics
from . import serializers, permissions
import core.models


class UploadView(BaseAPIView, DetailedCreateAPIView):
    """
    Can be used for small files without problems
    """
    serializer_class = serializers.UploadSerializer
    detail_serializer = serializers.FileSerializer

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        kwargs['space_qs'] = core.models.Space.objects.owned(self.request.user)
        return super().get_serializer(*args, **kwargs)


# TODO: Add Children to this view's serializer
class DetailFileView(BaseAPIView, generics.RetrieveAPIView):
    serializer_class = serializers.FileSerializer
    permission_classes = [permissions.FilePermission]
    lookup_url_kwarg = 'pk'
    queryset = core.models.File.objects.select_related('space', 'folder', 'parent')


class DeleteFileView(BaseAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.FilePermission]
    lookup_url_kwarg = 'pk'
    queryset = core.models.File.objects.select_related('space', 'folder', 'parent')


urlpatterns = [
    path('upload', UploadView.as_view(), name='file_upload'),
    path('<uuid:pk>', DetailFileView.as_view(), name='file_detail'),
    path('<uuid:pk>/delete', DeleteFileView.as_view(), name='file_delete'),
]
