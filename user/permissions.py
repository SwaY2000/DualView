from rest_framework import permissions


class IsOwnerAndAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
