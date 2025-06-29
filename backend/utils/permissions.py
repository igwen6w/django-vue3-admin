from rest_framework import permissions

class IsSuperUserOrReadOnly(permissions.BasePermission):
    """超级用户可读写，普通用户只读"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser
