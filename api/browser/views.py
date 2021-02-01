from django.urls import path
from rest_framework import generics
from api.generic import BaseAPIMixin
import core.models
from . import serializers


class ListFolderView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.FolderSerializer

    def get_queryset(self):
        return core.models.Folder.objects.select_related('space', 'parent').owned(self.request.user)

    def filter_queryset(self, qs):
        # TODO: Raise exception of parent_id or space_id does not exist or is not related to user
        space_id = self.kwargs['space_id']
        parent_id = self.kwargs.get('parent_id', None)
        return qs.filter(space_id=space_id, parent_id=parent_id)


class ListFileView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.FileSerializer

    def get_queryset(self):
        return core.models.File.objects.select_related('space', 'folder').owned(self.request.user)

    def filter_queryset(self, qs):
        # TODO: Raise exception of parent_id or space_id does not exist or is not related to user
        space_id = self.kwargs['space_id']
        folder_id = self.kwargs.get('folder_id', None)
        return qs.filter(space_id=space_id, folder_id=folder_id)


urlpatterns = [
    path('<uuid:space_id>/folders', ListFolderView.as_view(), name='browser_folder_root'),
    path('<uuid:space_id>/folders/<str:parent_id>', ListFolderView.as_view(), name='browser_folder'),
    path('<uuid:space_id>/files', ListFileView.as_view(), name='browser_file_root'),
    path('<uuid:space_id>/files/<str:folder_id>', ListFileView.as_view(), name='browser_file')
]
