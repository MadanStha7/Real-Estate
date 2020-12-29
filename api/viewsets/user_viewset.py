from rest_framework import viewsets

from api.serializers.user_serializer import UserProfileSerializer, AgentDetailSerializer
from user.models import UserProfile
from user.models import AgentDetail


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class AgentDetailViewSet(viewsets.ModelViewSet):
    queryset = AgentDetail.objects.all()
    serializer_class = AgentDetailSerializer
