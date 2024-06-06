from rest_framework import routers

from .viewsets import ProfileViewSet

app_name = 'users'

routers = routers.DefaultRouter()
routers.register('users', ProfileViewSet)
