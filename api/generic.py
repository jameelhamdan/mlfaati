from rest_framework import permissions, generics, response, status
from . import authentication


class BaseAPIView:
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]


class BaseDetailedView:
    detail_serializer = None

    def get_detail(self, serializer) -> dict:
        if self.detail_serializer:
            return self.detail_serializer(serializer.instance)
        return serializer.data


class DetailedUpdateAPIView(BaseDetailedView, generics.UpdateAPIView):
    detail_serializer = None

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return response.Response(self.get_detail(serializer))


class DetailedCreateAPIView(BaseDetailedView, generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return response.Response(self.get_detail(serializer), status=status.HTTP_201_CREATED, headers=headers)
