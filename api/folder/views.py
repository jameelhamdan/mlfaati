from django.urls import path
from rest_framework import generics, mixins, response, status
from django.utils.translation import gettext_lazy as _
from api.generic import (
    BaseAPIMixin, DetailedCreateAPIView, DetailedUpdateMixin
)
import core.models
from . import serializers, permissions


class CreateFolderView(BaseAPIMixin, DetailedCreateAPIView):
    serializer_class = serializers.CreateFolderSerializer
    detail_serializer_class = serializers.ExtendedFolderSerializer
    permission_classes = [permissions.FolderPermission]


class GenericFolderView(
        BaseAPIMixin,
        mixins.RetrieveModelMixin,
        DetailedUpdateMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):

    serializer_class = detail_serializer_class = serializers.ExtendedFolderSerializer
    update_serializer_class = serializers.UpdateFolderSerializer
    permission_classes = [permissions.FolderPermission]
    queryset = core.models.Folder.objects.select_related('space', 'parent')
    lookup_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

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
    path('<str:pk>', GenericFolderView.as_view(), name='folder'),
]
