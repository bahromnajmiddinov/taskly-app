from rest_framework import permissions


class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    '''
    Custom permission for UserViewSet to only allow owners of an object to edit it.
    Otherwise, GET or POST only.
    '''
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return obj == request.user
        return False
    