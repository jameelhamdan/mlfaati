from rest_framework import permissions


class PipelinePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if pipeline is related to user, `False` otherwise.
        """
        return obj.folder.space.owner_id == request.user.id
