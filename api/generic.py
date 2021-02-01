from rest_framework import permissions, generics, mixins, response, status
from . import authentication


class BaseAPIMixin:
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]


class BaseDetailedMixin:
    detail_serializer_class = None

    def get_detail(self, serializer) -> dict:
        if self.detail_serializer_class:
            return self.detail_serializer_class(serializer.instance).data
        return serializer.data


class DetailedUpdateMixin(BaseDetailedMixin, mixins.UpdateModelMixin):
    update_serializer_class = None

    def get_update_serializer(self, *args, **kwargs):
        serializer_class = self.get_update_serializer_class()
        kwargs.setdefault('context', self.get_update_serializer_class())
        return serializer_class(*args, **kwargs)

    def get_update_serializer_class(self):
        if self.update_serializer_class:
            return self.update_serializer_class
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_update_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return response.Response(self.get_detail(serializer))


class DetailedUpdateAPIView(DetailedUpdateMixin, generics.UpdateAPIView):
    pass


class DetailedCreateMixin(BaseDetailedMixin, mixins.CreateModelMixin):
    create_serializer_class = None

    def get_create_serializer(self, *args, **kwargs):
        serializer_class = self.get_create_serializer_class()
        kwargs.setdefault('context', self.get_create_serializer_class())
        return serializer_class(*args, **kwargs)

    def get_create_serializer_class(self):
        if self.create_serializer_class:
            return self.create_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_create_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return response.Response(self.get_detail(serializer), status=status.HTTP_201_CREATED, headers=headers)


class DetailedCreateAPIView(DetailedCreateMixin, generics.CreateAPIView):
    pass
