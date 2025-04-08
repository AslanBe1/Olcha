from rest_framework import permissions
from rest_framework.permissions import BasePermission


class CrudPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # return request.user and request.user.is_superuser
        return False