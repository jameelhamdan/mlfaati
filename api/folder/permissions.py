from rest_framework import permissions


class FolderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if folder is related to user, `False` otherwise.
        """
        return obj.space.owner_id == request.user.id
