from rest_framework import generics, response
from django.urls import path
from rest_framework.generics import get_object_or_404

import core.models
from . import serializers


class BaseBrowserView(generics.GenericAPIView):
    folder_serializer_class = serializers.FolderSerializer
    file_serializer_class = serializers.FileSerializer
    http_method_names = ['get']

    def get(self, *args, **kwargs):
        space = self.get_object()
        return self.retrieve(space, None, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(core.models.Space.objects.owned(self.request.user), pk=self.kwargs['pk'])

    def retrieve(self, space, folder, *args, **kwargs):
        folder_data = self.folder_serializer_class(folder).data if folder else None

        list_folders_data = self.folder_serializer_class(
            core.models.Folder.objects.filter(space=space, parent=folder),
            many=True
        ).data

        list_files_data = self.file_serializer_class(
            core.models.File.objects.filter(space=space, folder=folder),
            many=True
        ).data

        return response.Response({
            'current_folder': folder_data,
            'folders': list_folders_data,
            'files': list_files_data,
        })


class SpaceBrowserView(BaseBrowserView):
    """
    Gets Space root level direct folders and files descendents
    """
    pass


class FolderBrowserView(BaseBrowserView):
    """
    Gets Folder level direct folders and files descendents
    """
    def get_folder_object(self):
        return get_object_or_404(core.models.Folder.objects, space_id=self.kwargs['pk'], pk=self.kwargs['folder_id'])

    def get(self, *args, **kwargs):
        space = self.get_object()
        folder = self.get_folder_object()
        return super().retrieve(space, folder, *args, **kwargs)


urlpatterns = [
    path('browser/<int:pk>', BaseBrowserView.as_view(), name='api_browser'),
    path('browser/<int:pk>/<int:folder_id>', FolderBrowserView.as_view(), name='api_browser_folder'),
]
