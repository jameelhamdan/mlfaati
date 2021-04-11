from django.urls import path
from rest_framework import generics, mixins
from api.generic import BaseAPIMixin
import processing.models
from . import serializers, permissions


class ListPipelinesView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.PipelineSerializer

    def get_queryset(self):
        return processing.models.Pipeline.objects.owned(self.request.user)


class GenericPipelineView(BaseAPIMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = serializers.PipelineSerializer
    permission_classes = [permissions.PipelinePermission]
    lookup_url_kwarg = 'pk'
    queryset = processing.models.Pipeline.objects.select_related('folder', 'folder__space')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


urlpatterns = [
    path('list', ListPipelinesView.as_view(), name='pipeline_list'),
    path('<int:pk>', GenericPipelineView.as_view(), name='pipeline'),
]
