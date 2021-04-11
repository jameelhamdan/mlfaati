from rest_framework import permissions


class TransformationPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if transformation is related to user, `False` otherwise.
        """
        return obj.pipeline.folder.space.owner_id == request.user.id
