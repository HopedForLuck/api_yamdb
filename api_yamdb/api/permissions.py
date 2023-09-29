from rest_framework import permissions
from users.models import *

class IsSuperUserOrIsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == 'admin')
        )


class AnonimReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsSuperUserIsAdminIsModeratorIsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == 'admin'
                 or request.user.role == 'moderator'
                 or request.user == obj.author)
        )
