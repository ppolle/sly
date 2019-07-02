from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creators of a shortUrl object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user