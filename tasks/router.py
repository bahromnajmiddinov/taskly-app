from rest_framework import routers

from .viewsets import TaskListViewSet, TaskViewSet, AttachmentViewSet

app_name = 'tasks'

routers = routers.DefaultRouter()
routers.register('tasklists', TaskListViewSet)
routers.register('tasks', TaskViewSet)
routers.register('attachments', AttachmentViewSet)
