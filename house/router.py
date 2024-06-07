from rest_framework import routers

from .viewsets import HouseViewSet

app_name = 'house'

routers = routers.DefaultRouter()
routers.register('houses', HouseViewSet)
