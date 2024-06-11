from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from users.models import Profile
from .models import House
from .serializers import HouseSerializer
from .permissions import IsHouseManagerOrNone


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    permission_classes = [IsHouseManagerOrNone]
    serializer_class = HouseSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description',]
    ordering_fields = ['point', 'completed_tasks_count', 'notcompleted_tasks_count', 'created']
    filterset_fields = ['members',]
    
    @action(detail=True, methods=['POST'], name='Join', permission_classes=[])
    def join(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user
            if (user_profile.house == None):
                user_profile.house = house
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif (user_profile in house.members.all()):
                return Response({'detail': 'Already a member in this house'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Already a member in another house'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['POST'], name='Leave', permission_classes=[])
    def leave(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user
            if (user_profile.house == house):
                user_profile.house = None
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'Not a member in this house'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['POST'], name='Remove Member')
    def remove_member(self, request, pk=None):
        try:
            house = self.get_object()
            user_id = request.data.get('user_id', None)
            if (user_id == None):
                return Response({'user_id': 'Not provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            if (user_profile in house.members.all()):
                user_profile = Profile.objects.get(pk=user_id)
                user_profile.house = None
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'Not a member in this house'}, status=status.HTTP_400_BAD_REQUEST)

        except Profile.DoesNotExist as e:
            return Response({'detail': 'Provided user does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        