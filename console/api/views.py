from rest_framework import generics, response, permissions
from django.urls import path
from rest_framework.generics import get_object_or_404
from sql_util.aggregates import SubqueryCount, SubquerySum
import core.models
from . import serializers


class BaseBrowserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    folders_queryset = core.models.Folder.objects.annotate(
        files_count=SubqueryCount('files'),
        files_total_size=SubquerySum('files__content_length'),
    )
    files_queryset = core.models.File.objects.filter(
        parent_id__isnull=True
    ).select_related('space', 'folder', 'pipeline').prefetch_related('children')

    folder_serializer_class = serializers.FolderSerializer
    file_serializer_class = serializers.FileSerializer
    http_method_names = ['get']

    def get(self, *args, **kwargs):
        space = self.get_object()
        return self.retrieve(space, None, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(core.models.Space.objects.owned(self.request.user), pk=self.kwargs['pk'])

    def retrieve(self, space: 'core.models.Space', folder: ['core.models.Folder', None], *args, **kwargs):
        folder_data = self.folder_serializer_class(folder).data if folder else None

        if folder_data:
            folder_ancestors_data = self.folder_serializer_class(folder.ancestors(), many=True).data
            folder_data['ancestors'] = folder_ancestors_data

        list_folders_data = self.folder_serializer_class(
            self.folders_queryset.filter(space=space, parent=folder),
            many=True
        ).data

        list_files_data = self.file_serializer_class(
            self.files_queryset.filter(space=space, folder=folder),
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
        return get_object_or_404(self.folders_queryset, space_id=self.kwargs['pk'], pk=self.kwargs['folder_id'])

    def get(self, *args, **kwargs):
        space = self.get_object()
        folder = self.get_folder_object()
        return super().retrieve(space, folder, *args, **kwargs)


class AddFolderView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.AddFolderSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['space_qs'] = core.models.Space.objects.owned(self.request.user)
        return super().get_serializer(*args, **kwargs)


class UpdateFolderView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UpdateFolderSerializer

    def get_queryset(self):
        return core.models.Folder.objects.owned(self.request.user)


urlpatterns = [
    path('browser/<str:pk>', BaseBrowserView.as_view(), name='api_browser'),
    path('browser/<str:pk>/<int:folder_id>', FolderBrowserView.as_view(), name='api_browser_folder'),
    path('folder/add', AddFolderView.as_view(), name='api_folder_add'),
    path('folder/<int:pk>/update', UpdateFolderView.as_view(), name='api_folder_update'),
]
