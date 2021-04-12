from django.urls import path
from api.generic import BaseAPIMixin, DetailedCreateAPIView
import processing.models
from . import serializers, permissions
from rest_framework import generics, mixins


class CreateTransformationView(BaseAPIMixin, DetailedCreateAPIView):
    serializer_class = serializers.CreateTransformationSerializer
    detail_serializer_class = serializers.TransformationSerializer

    def get_create_serializer(self, *args, **kwargs):
        kwargs['pipeline_qs'] = processing.models.Pipeline.objects.owned(self.request.user)
        return super().get_serializer(*args, **kwargs)


class GenericTransformationView(
        BaseAPIMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):

    serializer_class = serializers.TransformationSerializer
    permission_classes = [permissions.TransformationPermission]
    lookup_url_kwarg = 'pk'
    queryset = processing.models.Transformation.objects.select_related('pipeline', 'pipeline__folder', 'pipeline__folder__space')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


urlpatterns = [
    path('', CreateTransformationView.as_view(), name='transformation'),
    path('/<int:pk>', GenericTransformationView.as_view(), name='transformation_object'),
]
