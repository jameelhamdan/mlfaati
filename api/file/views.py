from django.urls import path
from api.generic import BaseAPIMixin, DetailedCreateAPIView
from rest_framework import generics, mixins
from . import serializers, permissions
import core.models


class UploadView(BaseAPIMixin, DetailedCreateAPIView):
    """
    Can be used for small files without problems
    """
    serializer_class = serializers.UploadSerializer
    detail_serializer_class = serializers.FileSerializer

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_create_serializer(self, *args, **kwargs):
        kwargs['space_qs'] = core.models.Space.objects.owned(self.request.user)
        return super().get_serializer(*args, **kwargs)


class GenericFileView(BaseAPIMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = serializers.FileSerializer  # TODO: Add Children to this view's serializer
    permission_classes = [permissions.FilePermission]
    lookup_url_kwarg = 'pk'
    queryset = core.models.File.objects.select_related('space', 'folder', 'parent')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


urlpatterns = [
    path('upload', UploadView.as_view(), name='file_upload'),
    path('<uuid:pk>', GenericFileView.as_view(), name='file'),
]
