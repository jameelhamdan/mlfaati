from django.urls import path
from api.generic import BaseAPIMixin
import processing.models
from . import serializers, permissions
from rest_framework import generics, mixins


class GenericTransformationView(BaseAPIMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = serializers.TransformationSerializer
    permission_classes = [permissions.TransformationPermission]
    lookup_url_kwarg = 'pk'
    queryset = processing.models.Transformation.objects.select_related('pipeline', 'pipeline__folder', 'pipeline__folder__space')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


urlpatterns = [
    path('<int:pk>', GenericTransformationView.as_view(), name='transformation'),
]
