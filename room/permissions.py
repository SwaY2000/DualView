from rest_framework import permissions


class IsStuffAndAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff
