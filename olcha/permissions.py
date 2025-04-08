from rest_framework.permissions import BasePermission


class CrudPermission(BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_superuser or request.method == "GET"):
            return True
        return False