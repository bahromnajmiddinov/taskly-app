from rest_framework import permissions


class IsAllowedToEditTaskListElseNone(permissions.BasePermission):
    '''
    Custom permission for tasklistviewset to only allow the creator editing permission
    '''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_anonymous:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.created_by
    

class IsAllowedToEditTaskElseNone(permissions.BasePermission):
    '''
    Custom permission for taksviewset to only allow the members of house access to its task
    '''
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.user.house == obj.task_list.house
       
       
class IsAllowedToEditAttchmentElseNone(permissions.BasePermission):
    '''
    Custom permission for attachmentviewset to only allow the members of house access to its task
    '''
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.user.house == obj.task.task_list.house
    