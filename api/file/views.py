import os
from django.urls import path
from rest_framework import generics, mixins, exceptions
from rest_framework.generics import get_object_or_404
from api.generic import BaseAPIMixin, DetailedCreateAPIView
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

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        if 'pk' in self.kwargs.keys():
            return get_object_or_404(queryset, pk=self.kwargs['pk'])
        elif 'path' in self.kwargs.keys() and 'space_name' in self.kwargs.keys():
            space_name = self.kwargs['space_name']
            dir_name, file_name = os.path.split(self.kwargs['path'])
            given_path = dir_name.split(core.models.DIRECTORY_SEPARATOR) if dir_name != '' else None

            return get_object_or_404(
                queryset, space__name=space_name, folder__path=given_path, name=file_name
            )

        raise exceptions.ParseError('Requested kwarg is not allowed')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


urlpatterns = [
    path('', UploadView.as_view(), name='file_upload'),
    path('/upload', UploadView.as_view(), name='file_upload_alt'),
    path('/<uuid:pk>', GenericFileView.as_view(), name='file'),
    path('/<str:space_name>/<path:path>', GenericFileView.as_view(), name='file_by_path'),

]
