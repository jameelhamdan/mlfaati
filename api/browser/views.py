from django.urls import path
from rest_framework import generics, exceptions
from api.generic import BaseAPIMixin
import core.models
from . import serializers


QUERY_TYPE_ID = 'id'
QUERY_TYPE_NAME = 'name'
QUERY_TYPES = [QUERY_TYPE_ID, QUERY_TYPE_NAME]


class ListFolderView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.FolderSerializer

    def get_queryset(self):
        return core.models.Folder.objects.select_related('space', 'parent').owned(self.request.user)

    def filter_queryset(self, qs):
        # TODO: Raise exception of parent_id or space_id does not exist or is not related to user
        space_id = self.kwargs['space_id']
        parent_id = self.kwargs.get('parent_id', None)
        query_type = self.request.GET.get('by')

        if not query_type or query_type not in QUERY_TYPES:
            query_type = QUERY_TYPE_ID

        if query_type == QUERY_TYPE_NAME:
            qs = qs.filter(space__name=space_id)
        elif query_type == QUERY_TYPE_ID:
            qs = qs.filter(space_id=space_id)
        else:
            raise exceptions.ParseError('Unknown query type.')

        return qs.filter(parent_id=parent_id)


class ListFileView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.FileSerializer

    def get_queryset(self):
        return core.models.File.objects.select_related('space', 'folder').owned(self.request.user)

    def filter_queryset(self, qs):
        # TODO: Raise exception of parent_id or space_id does not exist or is not related to user
        space_id = self.kwargs['space_id']
        folder_id = self.kwargs.get('folder_id', None)

        query_type = self.request.GET.get('by')

        if not query_type or query_type not in QUERY_TYPES:
            query_type = QUERY_TYPE_ID

        if query_type == QUERY_TYPE_NAME:
            qs = qs.filter(space__name=space_id)

        elif query_type == QUERY_TYPE_ID:
            qs = qs.filter(space_id=space_id)
        else:
            raise exceptions.ParseError('Unknown query type.')

        return qs.filter(folder_id=folder_id)


urlpatterns = [
    path('<str:space_id>/folders', ListFolderView.as_view(), name='browser_folder_root'),
    path('<str:space_id>/folders/<str:parent_id>', ListFolderView.as_view(), name='browser_folder'),
    path('<str:space_id>/files', ListFileView.as_view(), name='browser_file_root'),
    path('<str:space_id>/files/<str:folder_id>', ListFileView.as_view(), name='browser_file')
]
