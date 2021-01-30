from django.urls import path
from api.generic import BaseAPIView, DetailedCreateAPIView
from . import serializers
import core.models


class UploadView(BaseAPIView, DetailedCreateAPIView):
    """
    Can be used for small files without problems
    """
    serializer_class = serializers.UploadSerializer
    detail_serializer = serializers.FileSerializer

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        kwargs['space_qs'] = core.models.Space.objects.owned(self.request.user)
        return super().get_serializer(*args, **kwargs)


urlpatterns = [
    path('upload', UploadView.as_view(), name='file_upload'),
]
