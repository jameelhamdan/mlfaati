from django.urls import path
from rest_framework import generics
from api.generic import BaseAPIView
import core.models
from . import serializers, permissions


class ListFolderView(BaseAPIView, generics.ListAPIView):
    serializer_class = serializers.FolderSerializer

    def get_queryset(self):
        return core.models.Folder.objects.select_related('space', 'parent').owned(self.request.user)

    def filter_queryset(self, queryset):
        # TODO: Raise exception of parent_id does not exist or is not related to user
        parent_id = self.kwargs.get('parent_id')
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        return queryset


class DetailFolderView(BaseAPIView, generics.RetrieveAPIView):
    serializer_class = serializers.ExtendedFolderSerializer
    permission_classes = [permissions.FolderPermission]
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return core.models.Folder.objects.select_related('space', 'parent')


class UpdateFolderView(BaseAPIView, generics.UpdateAPIView):
    serializer_class = serializers.UpdateFolderSerializer
    permission_classes = [permissions.FolderPermission]

    def get_queryset(self):
        return core.models.Folder.objects.select_related('space', 'parent')


class CreateFolderView(BaseAPIView, generics.CreateAPIView):
    serializer_class = serializers.CreateFolderSerializer
    permission_classes = [permissions.FolderPermission]


urlpatterns = [
    path('list/', ListFolderView.as_view(), name='folder_list'),
    path('list/<str:parent_id>', ListFolderView.as_view(), name='folder_children_list'),
    path('detail/<str:pk>', DetailFolderView.as_view(), name='folder_detail'),
    path('update/<str:pk>', UpdateFolderView.as_view(), name='folder_update'),
    path('create', CreateFolderView.as_view(), name='folder_create'),
]
