from rest_framework import viewsets

from .models import Profile
from .serializers import ProfileSerializer
from .permissions import IsUserOwnerOrGetAndPostOnly


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserOwnerOrGetAndPostOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
