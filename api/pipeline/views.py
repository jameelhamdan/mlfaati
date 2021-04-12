from django.urls import path
from rest_framework import generics, mixins, response
from api.generic import BaseAPIMixin, DetailedCreateAPIView, DetailedUpdateMixin
import processing.models
import core.models
from . import serializers, permissions


class ListCreatePipelineView(BaseAPIMixin, DetailedCreateAPIView):
    serializer_class = serializers.PipelineSerializer
    detail_serializer_class = serializers.ExtendedPipelineSerializer

    def get_queryset(self):
        return processing.models.Pipeline.objects.owned(self.request.user)

    def get_create_serializer(self, *args, **kwargs):
        kwargs['folder_qs'] = core.models.Folder.objects.owned(self.request.user)
        return super().get_serializer(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class GenericPipelineView(
        BaseAPIMixin,
        mixins.RetrieveModelMixin,
        DetailedUpdateMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):

    serializer_class = serializers.PipelineSerializer
    update_serializer_class = serializers.UpdatePipelineSerializer
    detail_serializer_class = serializers.ExtendedPipelineSerializer
    permission_classes = [permissions.PipelinePermission]
    queryset = processing.models.Pipeline.objects.select_related('folder', 'folder__space').prefetch_related('transformations')
    lookup_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.detail_serializer_class(instance=instance)
        return response.Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


urlpatterns = [
    path('', ListCreatePipelineView.as_view(), name='pipeline'),
    path('/<int:pk>', GenericPipelineView.as_view(), name='pipeline_object'),
]
