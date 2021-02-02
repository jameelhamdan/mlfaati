from django.urls import path
from rest_framework import generics
from api.generic import BaseAPIMixin
import core.models
from . import serializers


class ListSpaceView(BaseAPIMixin, generics.ListAPIView):
    serializer_class = serializers.SpaceSerializer

    def get_queryset(self):
        return core.models.Space.objects.owned(self.request.user)


urlpatterns = [
    path('list', ListSpaceView.as_view(), name='list'),
]
